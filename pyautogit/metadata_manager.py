"""Metadata Management Classes and Functions
"""

import os
import json
import shutil
import pyautogit
import pyautogit.logger as LOGGER

class PyAutogitMetadataManager:
    """Helper class for managing inter-use metadata for pyautogit

    Attributes
    ----------
    manager : PyAutogitManager
        The top level program manager object
    first_time : bool
        Flag that tells metadata manager if metadata exists
    """

    def __init__(self, manager):
        """Constructor for PyAutogitMetadataManager
        """

        self.manager = manager
        self.first_time = False


    def write_metadata(self):
        """Writes metadata file with cached settings
        """

        settings_dir = os.path.join(self.manager.workspace_path, '.pyautogit')
        settings_file = os.path.join(settings_dir, 'pyautogit_settings.json')
        if not os.path.exists(settings_dir):
            os.mkdir(settings_dir)
        if os.path.exists(settings_file):
            os.remove(settings_file)
        metadata = {}
        metadata['EDITOR']      = self.manager.default_editor
        metadata['VERSION']     = pyautogit.__version__
        metadata['LOG_ENABLE']  = LOGGER._LOG_ENABLED
        LOGGER.write('Writing metadata: {}'.format(metadata))
        fp = open(settings_file, 'w')
        json.dump(metadata, fp)
        fp.close()


    def apply_metadata(self, metadata):
        """Applies metadata from cached settings

        Parameters
        ----------
        metadata : dict
            Metadata parsed from json to python dict.
        """
        if metadata is None:
            return
        if 'EDITOR' in metadata.keys():
            self.manager.default_editor = metadata['EDITOR']
            self.manager.editor_type = 'External'
        if 'VERSION' in metadata.keys() and metadata['VERSION'] != pyautogit.__version__:
            self.manager.root.show_message_popup('PyAutogit Updated', 'Congratulations for updating to pyautogit {}! See patch notes on github.'.format(pyautogit.__version__))
        if 'LOG_ENABLE' in metadata.keys() and metadata['LOG_ENABLE']:
            #LOGGER.toggle_logging()
            pass


    def read_metadata(self):
        """Converts metadata json file to python dict

        Returns
        -------
        metadata : dict
            metadata dictionary
        """

        settings_dir = os.path.join(self.manager.workspace_path, '.pyautogit')
        settings_file = os.path.join(settings_dir, 'pyautogit_settings.json')
        if os.path.exists(settings_file):
            try:
                fp = open(settings_file, 'r')
                metadata = json.load(fp)
                fp.close()
                LOGGER.write('Read metadata:{}'.format(metadata))
                return metadata
            except json.decoder.JSONDecodeError:
                shutil.rmtree(settings_dir)
                self.first_time = True
        else:
            self.first_time = True
            
