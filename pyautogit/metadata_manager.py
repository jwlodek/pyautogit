"""Metadata Management Classes and Functions
"""

class PyAutogitMetadataManager:
    """Helper class for managing inter-use metadata for pyautogit

    Attributes
    ----------
    manager : PyAutogitManager
        The top level program manager object
    first_time : bool
        Flag that tells metadata manager if metadata exists

    Methods
    -------
    write_metadata()
        Writes metadata file with cached settings
    apply_metadata()
        Applies metadata from cached settings
    read_metadata()
        Converts metadata json file to python dict
    """

    def __init__(self, manager):
        """Constructor for PyAutogitMetadataManager
        """

        self.manager = manager
        self.first_time = False


    def write_metadata(self):
        """Writes metadata file with cached settings
        """

        settings_dir = os.path.join(self.manager.top_path, '.pyautogit')
        settings_file = os.path.join(settings_dir, 'pyautogit_settings.json')
        if not os.path.exists(settings_dir):
            os.mkdir(settings_dir)
        if os.path.exists(settings_file):
            os.remove(settings_file)
        metadata = {}
        metadata['EDITOR'] = self.manager.default_editor
        metadata['VERSION'] = __version__
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
        if 'VERSION' in metadata.keys() and metadata['VERSION'] != __version__:
            self.manager.root.show_message_popup('PyAutogit Updated', 'Congratulations for updating to pyautogit {}! See patch notes on github.'.format(__version__))
    
    def read_metadata(self):
        """Converts metadata json file to python dict

        Returns
        -------
        metadata : dict
            metadata dictionary
        """

        settings_dir = os.path.join(self.manager.top_path, '.pyautogit')
        settings_file = os.path.join(settings_dir, 'pyautogit_settings.json')
        if os.path.exists(settings_file):
            try:
                fp = open(settings_file, 'r')
                metadata = json.load(fp)
                fp.close()
                return metadata
            except json.decoder.JSONDecodeError:
                shutil.rmtree(settings_dir)
                self.first_time = True
        else:
            self.first_time = True
            
