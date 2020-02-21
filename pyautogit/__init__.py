"""Main pyautogit manager class and entry point

The main driver class contains code for common actions performed by all subscreens such as
credential management, as well as functions for switching between subscreens.

Author: Jakub Wlodek  
Created: 01-Oct-2019

Classes
-------
PyAutogitManager
    Main py_cui wrapper class that drives pyautogit. Uses ScreenManager subclass instances for subscreens

Functions
---------
find_repos_in_path()
    Searches for .git directories in specified path
is_git_repo()
    Checks if given path is a git repository
parse_args()
    Parses user arguments
main()
    Program entrypoint
"""

# Core Python Utilities
import argparse
import getpass
import json
import os
import shutil
import subprocess
import threading
import datetime
from subprocess import Popen, PIPE

# py_cui library used for Command Line UI construction
import py_cui

# Subscreens and pyautogit modules
import pyautogit.logger as LOGGER
import pyautogit.repo_select_screen as SELECT
import pyautogit.repo_control_screen as CONTROL
import pyautogit.internal_editor_screen as EDITOR
import pyautogit.settings_screen as SETTINGS
import pyautogit.metadata_manager as METADATA


# Module version + copyright
__version__     = '0.0.3'
__copyright__   = '2019-2020'


# Helper pyautogit functions

def find_repos_in_path(path):
    """Helper function that finds repositories in the path

    Parameters
    ----------
    path : str
        Target path
    
    Returns
    -------
    repos : list of str
        list of git repositories within target
    """

    repos = []
    for dir in os.listdir(path):
        new_dir = os.path.join(path, dir)
        if os.path.isdir(new_dir) and is_git_repo(new_dir):
            repos.append(os.path.basename(new_dir))

    LOGGER.write('Found repos in path: {}'.format(repos))

    return repos


def is_git_repo(path):
    """Simple function that checks if a given path is a git repository

    Parameters
    ----------
    path : str
        path to check
    
    Returns
    -------
    is_repo : bool
        True if .git exists, False otherwise
    """

    is_repo = False
    if os.path.exists(os.path.join(path, '.git')):
        is_repo = True
    return is_repo


def parse_args():
    """Function that parses user arguments for pyautogit

    Returns
    -------
    target_repo : str
        The target path for pyautogit
    save_metadata : bool
        flag to say if metadata should be saved
    credentials : list of str
        username, password, if entered
    """

    target_repo = '.'
    credentials = []

    parser = argparse.ArgumentParser(description="A command line interface for git commands.")
    parser.add_argument('-c', '--credentials',      action='store_true', help='Allows user to enter credentials once when pyautogit is started.')
    parser.add_argument('-w', '--workspace',        help='Pass a path to this argument to start pyautogit in a workspace not the current directory.')
    parser.add_argument('-n', '--nosavemetadata',   action='store_true', help='Add this flag if you would like pyautogit to not save metadata between sessions.')
    parser.add_argument('-d', '--debug',            action='store_true', help='Flag that enables debug logging by default.')
    parser.add_argument('-v', '--version',          action='store_true', help='Run pyautogit with this flag to print version information.')
    args = vars(parser.parse_args())

    if args['version']:
        print('pyautogit v{}\n'.format(__version__))
        print('BSD-3-Clause License')
        print('Copyright (c) {} Jakub Wlodek'.format(__copyright__))
        print('https://github.com/jwlodek/pyautogit\n')
        exit()

    if args['credentials']:
        user = input('Please enter your github/gitlab username > ')
        credentials.append(user)
        passwd = getpass.getpass(prompt="Please enter your github/gitlab password > ")
        credentials.append(passwd)
    if args['workspace'] is not None:
        if os.path.exists(args['workspace']):
            if os.path.isdir(args['workspace']):
                os.chdir(args['workspace'])
            else:
                print('ERROR - Path {} is not a directory.'.format(args['workspace']))
                exit(-1)
        else:
            print('ERROR - Path {} does not exist.'.format(args['workspace']))
            exit(-1)

    return target_repo, credentials, args


def main():
    """Entry point for pyautogit. Parses arguments, and initializes the CUI
    """

    target, credentials, args = parse_args()
    save_metadata = not args['nosavemetadata']
    debug_logging = args['debug']

    target_abs = os.path.abspath(target)

    input_type = 'repo'
    if not is_git_repo(target):
        input_type = 'workspace'

    # Make sure we have write permissions
    if not os.access(target, os.W_OK):
        print('ERROR - Permission error for target {}'.format(target_abs))
        exit(-1)
    if input_type == 'repo' and not os.access(os.path.dirname(target_abs), os.W_OK):
        print('ERROR - Permission denied for parent workspace {} of repository {}'.format(os.path.dirname(target_abs), target_abs))
        exit(-1)

    if debug_logging:
        if input_type=='repo':
            LOGGER.set_log_file_path('../.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]))
        else:
            LOGGER.set_log_file_path('.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]))
        LOGGER.toggle_logging()
        LOGGER.write('Initialized debug logging')

    root = py_cui.PyCUI(5, 4)
    manager = PyAutogitManager(root, target, input_type, save_metadata, credentials)
    
    LOGGER.write('Parsed args. Target location - {}'.format(target_abs))
    LOGGER.write('Initial state - {}'.format(input_type))
    LOGGER.write('Initialized manager object, starting CUI...')

    root.start()


# Main pyautogit mananger class


class PyAutogitManager:
    """Main pyautogit manager class. Controls all operations of CUI

    Attributes
    ----------
    root : PyCUI
        The root py_cui window
    target_path : str
        The path to the workspace directory
    save_metadata : bool
        Flag to specify metadata saving or not
    credentials : list of str
        Username and Password for git remote
    current_state : str
        Current state of pyautogit (repo control or repo select)
    default_editor : str
        Command to open external editor
    post_input_callback : no-arg or lambda function
        Function fired after a user input event
    operation_thread : Thread
        A thread for performing async operations. Starts as None, Thread created as needed
    repos : list of str
        List of repositories found in workspace
    repo_select_widget_set : py_cui.widget_set.WidgetSet
        set of py_cui widgets that are parts of the repo select screen
    repo_menu : py_cui.widgets.ScrollMenu
        The repository select menu in the repo select screen
    git_status_box : py_cui.widgets.ScrolledTextBlock
        Main info panel for repo select screen
    current_status_box : py_cui.widgets.ScrolledTextBlock
        Secondary info panel for repo select screen
    clone_new_box : py_cui.widgets.TextBox
        Textbox for cloning new repositories
    create_new_box : py_cui.widgets.TextBox
        Textbox for creating new repositories
    repo_select_manager : RepoSelectManager
        The manager wrapper class for the repo select screen
    repo_control_widget_set : py_cui.widget_set.WidgetSet
        set of py_cui widgets that are parts of the repo control screen
    add_files_menu : py_cui.widgets.ScrollMenu
        Menu for adding/unstaging files
    remotes_menu : py_cui.widgets.ScrollMenu
        Menu for selecting remotes
    branch_menu : py_cui.widgets.ScrollMenu
        Menu for selecting branches
    commits_menu : py_cui.widgets.ScrollMenu
        Menu listing most recent commits
    info_text_block : py_cui.widgets.ScrolledTextBlock
        Main Info text block in repo control screen
    new_branch_textbox : py_cui.widgets.TextBox
        Textbox for creating new branches
    commit_message_box : py_cui.widgets.TextBox
        Textbox for entering new commit messages
    repo_control_manager : RepoControlManager
        Manager wrapper for repo control screen

    Methods
    -------
    open_not_supported_popup()
        Function that displays warning for a non-supported operation
    open_autogit_window()
        Function that opens the repository control window.
    open_repo_select_window()
        Function that opens the repository select window.
    update_password()
        Function called once password is entered.
    ask_password()
        Function that opens popup and asks for password. Also writes username to credentials
    ask_credentials()
        Function that asks for user credentials and places them in the appropriate variables.
    were_credentials_entered()
        Simple function for checking if credentials were entered
    perform_long_operation()
        Function that wraps an operation around a loading icon popup.
    update_default_editor()
        Function that sets the default editor
    ask_default_editor()
        Function that asks user to enter a default text editor
    update_message()
        Function that is run after user inputs message
    ask_message()
        Function that asks the user for input.
    get_logo_text()
        Generates ascii-art version of pyautogit logo
    get_about_info()
        Generates some about me information
    get_welcome_message()
        Function that gets a basic welcome message shown at first run
    """

    def __init__(self, root, target_path, current_state, save_metadata, credentials):
        """Constructor for PyAutogitManager
        """

        self.root = root
        self.repo_select_manager    = SELECT.RepoSelectManager(self)
        self.repo_control_manager   = CONTROL.RepoControlManager(self)
        self.settings_manager       = SETTINGS.SettingsScreen(self)
        self.editor_manager         = EDITOR.EditorScreenManager(self, target_path)
        LOGGER.write('Initialized subscreen managers.')

        self.save_metadata = save_metadata

        # Make sure to convert to absolute path. If we opened a repository, the top path will be one level higher
        self.current_path   = os.path.abspath(target_path)
        self.workspace_path = self.current_path
        if current_state == 'repo':
            self.workspace_path = os.path.dirname(self.current_path)
        
        # Setup some helper objects and default information/variables
        self.current_state  = current_state
        self.default_editor = None
        self.editor_type    = 'Internal'
        
        self.metadata_manager   = METADATA.PyAutogitMetadataManager(self)
        self.loaded_metadata    = self.metadata_manager.read_metadata()
        LOGGER.write('Loaded metadata')
        LOGGER.write(self.loaded_metadata)
        self.metadata_manager.apply_metadata(self.loaded_metadata)
        LOGGER.write('Applied metadata')

        # Stores currently entered credentials
        self.credentials = credentials

        # Temp variable fired on callback after inout
        self.post_input_callback = None

        # Add a run on exit callback to save metadata and close log file
        self.root.run_on_exit(self.close_cleanup)

        # Utility variable used to store user input for callbacks
        self.user_message = None

        # Thread used to perform longer operations
        self.operation_thread = None

        # Repository select screen widgets, key commands.
        self.repos = find_repos_in_path(self.workspace_path)

        # Initialize CUI elements for each sub-screen
        self.repo_select_widget_set     = self.repo_select_manager.initialize_screen_elements()
        self.repo_control_widget_set    = self.repo_control_manager.initialize_screen_elements()
        self.settings_widget_set        = self.settings_manager.initialize_screen_elements()
        self.editor_widget_set          = self.editor_manager.initialize_screen_elements()
        LOGGER.write('Initialized CUI elements')

        # Open repo select screen in workspace view
        if self.current_state == 'workspace':
            self.open_repo_select_window()

        # Open repo control screen in repo view
        elif self.current_state == 'repo':
            self.open_autogit_window()


    def close_cleanup(self):
        """Function fired upon closing pyautogit
        """

        if self.save_metadata:
            self.metadata_manager.write_metadata()
        LOGGER.close_logger()


    def clean_exit(self):
        """Function that exits the CUI cleanly
        """

        LOGGER.write('Exiting pyautogit.')
        self.close_cleanup()
        exit()


    def error_exit(self):
        """Function that exits the CUI with an error code
        """

        LOGGER.write('Exiting with error!')
        self.close_cleanup()
        exit(-1)


    def open_not_supported_popup(self, operation):
        """Function that displays warning for a non-supported operation

        Parameters
        ----------
        operation : str
            The name of the non-supported operation
        """

        self.root.show_warning_popup('Warning - Not Supported', 'The {} operation is not yet supported.'.format(operation))


    def open_autogit_window(self):
        """Function that opens the repository control window.
        """

        LOGGER.write('Opening repo control window')
        target = self.repo_select_manager.repo_menu.get()
        self.repo_select_manager.clear_elements()
        self.repo_control_manager.set_initial_values()
        
        self.root.apply_widget_set(self.repo_control_widget_set)
        if self.current_state == 'workspace':
            os.chdir(target)
        self.current_state = 'repo'
        self.root.set_title('pyautogit v{} - {}'.format(__version__, target))
        self.repo_control_manager.refresh_status()


    def open_autogit_window_target(self):
        """Function that opens a repo control window given a target location
        """

        LOGGER.write('Opening autogit control window on target dir.')
        self.repo_select_manager.clear_elements()
        self.repo_control_manager.set_initial_values()
        self.root.apply_widget_set(self.repo_control_widget_set)
        self.repo_control_manager.refresh_status()


    def open_repo_select_window(self):
        """Opens the repo select window. Fired when the backspace key is pressed in the repo control window
        """

        LOGGER.write('Opening repo select window')
        self.repo_control_manager.clear_elements()
        self.settings_manager.clear_elements()
        self.repo_select_manager.set_initial_values()
        
        self.root.apply_widget_set(self.repo_select_widget_set)
        if self.current_state == 'repo':
            os.chdir('..')
        self.current_state = 'workspace'
        self.root.set_title('pyautogit v{} - {}'.format(__version__, os.path.basename(os.getcwd())))
        self.repo_select_manager.refresh_status()
        self.root.move_focus(self.repo_select_manager.repo_menu)


    def open_settings_window(self):
        """Function for opening the settings window
        """

        LOGGER.write('Opening settings window')
        self.repo_select_manager.clear_elements()
        self.settings_manager.set_initial_values()
        self.root.apply_widget_set(self.settings_widget_set)
        self.root.set_title('pyautogit v{} Settings'.format(__version__))
        self.current_state = 'settings'
        self.settings_manager.refresh_status()


    def open_editor_window(self):
        """Function that opens an editor window
        """

        LOGGER.write('Opening Editor Window')
        self.editor_manager.open_new_directory_external(os.getcwd())
        self.editor_manager.set_initial_values()
        self.root.apply_widget_set(self.editor_widget_set)
        self.current_state == 'editor'
        self.editor_manager.refresh_status()
        self.root.move_focus(self.editor_manager.file_menu)
    

    #-------------------------------------------
    # Credential handler functions
    #-------------------------------------------


    def update_password(self, passwd):
        """Function called once password is entered. 

        If necessary, fires the post_input_callback function

        Parameters
        ----------
        passwd : str
            The user's password
        """

        self.credentials.append(passwd)
        self.repo_select_manager.refresh_status()
        LOGGER.write('User credentials entered')
        if self.post_input_callback is not None:
            self.post_input_callback()
        self.post_input_callback = None


    def ask_password(self, user):
        """Function that opens popup and asks for password. Also writes username to credentials.

        Parameters
        ----------
        user : str
            The user's username
        """

        self.credentials.append(user)
        self.root.show_text_box_popup('Please enter your git remote password', self.update_password, password=True)


    def ask_credentials(self, callback=None):
        """Function that asks for user credentials and places them in the appropriate variables.

        Parameters
        ----------
        callback : function
            Default None, otherwise function called after credentials are entered.
        """

        del self.credentials[:]
        if callback is not None:
            self.post_input_callback = callback
        self.root.show_text_box_popup('Please enter your git remote username', self.ask_password)



    def were_credentials_entered(self):
        """Simple function for checking if credentials were entered

        Returns
        -------
        were_credentials_entered : bool
            True if credentials found, otherwise false
        """

        return len(self.credentials) == 2


    def perform_long_operation(self, title, long_operation_function, post_loading_callback):
        """Function that wraps an operation around a loading icon popup.

        Parameters
        ----------
        title : str
            title for loading icon
        long_operation_function : function
            operation to perform in the background
        post_loading_callback : function
            Function fired once long operation is finished.
        """

        LOGGER.write('Executing long operation {}'.format(title))
        self.root.show_loading_icon_popup('Please Wait', title, callback = post_loading_callback)
        self.operation_thread = threading.Thread(target=long_operation_function)
        self.operation_thread.start()


    def update_default_editor(self):
        """Function that sets the default editor

        Parameters
        ----------
        editor : str
            command line call to open the editor
        """

        LOGGER.write('Updating the default editor to {}'.format(self.user_message))
        self.default_editor = self.user_message
        self.editor_type = 'External'
        self.root.show_message_popup('Default Editor Changed', '{} editor will be used to open directories'.format(self.user_message))
        self.repo_select_manager.refresh_status()


    def ask_default_editor(self):
        """Function that asks user to enter a default text editor
        """

        self.ask_message('Please enter a default editor command. (Ex. code, emacs)', callback=self.update_default_editor)


    def update_message(self, message):
        """Function that is run after user inputs message
        
        Parameters
        ----------
        message : str
            User returned input
        """

        self.user_message = message
        if self.post_input_callback is not None:
            self.post_input_callback()
        self.post_input_callback = None


    def ask_message(self, prompt, callback=None):
        """Function that asks the user for input.
        
        Parameters
        ----------
        prompt : str
            Prompt for user input
        callback : function
            Default None, otherwise, function fired after credentials are asked
        """

        if callback is not None:
            self.post_input_callback = callback
        self.root.show_text_box_popup(prompt, self.update_message)


    def get_logo_text(self):
        """Generates ascii-art version of pyautogit logo

        Returns
        -------
        logo : str
            ascii-art logo
        """

        logo =         '         _    _ _______ ____   _____ _____ _______\n'
        logo = logo +  '    /\\  | |  | |__   __/ __ \\ / ____|_   _|__   __|\n'
        logo = logo +  '   /  \\ | |  | |  | | | |  | | |  __  | |    | |   \n'
        logo = logo +  '  / /\\ \\| |  | |  | | | |  | | | |_ | | |    | |   \n'
        logo = logo +  ' / ____ \\ |__| |  | | | |__| | |__| |_| |_   | |   \n'
        logo = logo +  '/_/    \\_\\____/   |_|  \\____/ \\_____|_____|  |_|   \n'
        return logo


    def get_about_info(self, with_logo=True):
        """Generates some about me information

        Parameters
        ----------
        with_logo : bool
            flag to show logo or not.
        
        Returns
        -------
        about_info : str
            string with about information
        """

        if with_logo:
            about_info = self.get_logo_text() + '\n\n\n'
        else:
            about_info = '\n'
        about_info = about_info + 'Author: Jakub Wlodek\n\nPython CUI git client: https://github.com/jwlodek/pyautogit\n\n\n'
        about_info = about_info + 'Powered by the py_cui Python Command Line UI library:\n\n'
        about_info = about_info + 'https://github.com/jwlodek/py_cui\n\n\n'
        about_info = about_info + 'Documentation available here:\n\n'
        about_info = about_info + 'pyautogit: https://jwlodek.github.io/pyautogit-docs\n'
        about_info = about_info + 'py_cui:    https://jwlodek.github.io/py_cui-docs\n\n\n'
        about_info = about_info + 'Star me on Github!\n\n'
        about_info = about_info + 'Copyright (c) {} Jakub Wlodek'.format(__copyright__)
        return about_info


    def get_welcome_message(self):
        """Function that gets a basic welcome message shown at first run
        
        Returns
        -------
        welcome : str
            welcome message string
        """

        welcome = '\nWelcome to pyautogit!\n\nThis is a command line interface for working with git projects.\n'
        welcome = welcome + '\nTo begin, take a look at the repositories list to the right.\nThis shows all detected '
        welcome = welcome + 'repositories in the workspace.\nYou may create new repositories, or clone them also to the right.\n'
        welcome = welcome + '\nFor pushing, pulling, and cloning, you will need to enter credentials.\nDo this by pressing "c".\n'
        welcome = welcome + '\nAlso, to set a default editor (that can open files and dirs),\npress "e".\n'
        welcome = welcome + '\nIf you encounter issues, please make a ticket on the github page,\nand if you enjoy pyautogit,'
        welcome = welcome + 'feel free to give\nit a star or a sponsorship.\n\nIf you would like to contribute, feel free to do so as well!'
        return welcome