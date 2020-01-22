"""Module containing logging classes and functions.

The logger is controlled via a set of global variables set by the pyautogit client.
"""

import os
import datetime

# Global var that stores path to logfile
_LOG_FILE_PATH = None

# Global var that stores whether or not logging is enabled
_LOG_ENABLED = False

# Global var that stores file pointer for log file
_LOG_FILE_POINTER = None


def toggle_logging():
    """Function for opening/closing log file as required.
    """

    global _LOG_ENABLED
    global _LOG_FILE_PATH
    if _LOG_FILE_PATH is None and not _LOG_ENABLED:
        return
    if _LOG_ENABLED:
        close_logger()
        _LOG_ENABLED = False
    elif not os.path.exists(os.path.dirname(_LOG_FILE_PATH)):
        return
    else:
        if _LOG_FILE_PATH is not None and os.access(os.path.dirname(_LOG_FILE_PATH), os.W_OK):
            initialized = initialize_logger()
            _LOG_ENABLED = initialized
        else:
            return
                

def set_log_file_path(log_file_path):
    """Sets the path to the log file

    Parameters
    ----------
    log_file_path : str
        Path to the log file
    """

    global _LOG_FILE_PATH
    _LOG_FILE_PATH = log_file_path


def initialize_logger():
    """Function for initializing log-file writing in addition to stdout output

    Returns
    -------
    initialized : bool
        True if log file opened, false otherwise
    """

    global _LOG_FILE_PATH
    global _LOG_FILE_POINTER
    if os.path.exists(_LOG_FILE_PATH):
        if not os.access(_LOG_FILE_PATH, os.W_OK):
            return False
    _LOG_FILE_POINTER = open(_LOG_FILE_PATH, 'w+')
    return True


def close_logger():
    """Function that closes the opened logfile
    """

    global _LOG_FILE_POINTER
    if _LOG_FILE_POINTER is not None:
        _LOG_FILE_POINTER.close()
        _LOG_FILE_POINTER = None



def write(text, no_timestamp=False):
    """Main logging funcion. Called if write function was set
    
    Parameters
    ----------
    text : str
        debug text to print
    no_timestamp=False : bool
        a flag to disable timestamp printing when required
    """

    global _LOG_FILE_POINTER
    global _LOG_ENABLED
    if _LOG_ENABLED and _LOG_FILE_POINTER is not None:

        # remove timestamp if not in use
        if no_timestamp:
            final_text = '{}\n'.format(text)
        else:
            # otherwise add timestamp
            final_text = '{} - {}\n'.format(datetime.datetime.now(), text)

        _LOG_FILE_POINTER.write(final_text)

