"""File containing entry point for pyautogit, as well as a top level class for managing the program.

It also contains some helper functions and argument parsing.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

# Core Python Utilities
import argparse
import getpass
import json
import os
import shutil
import subprocess
import threading
from subprocess import Popen, PIPE

# py_cui library used for Command Line UI construction
import py_cui

# Subscreens
import pyautogit.repo_select_screen as RepoSelect
import pyautogit.repo_control_screen as RepoControl


# Module version
__version__='0.0.1'


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
        Manager wrapper for repo control screen.

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
        self.repo_select_manager = RepoSelect.RepoSelectManager(self)
        self.repo_control_manager = RepoControl.RepoControlManager(self)

        # Make sure to convert to absolute path. If we opened a repository, the top path will be one level higher
        self.current_path = os.path.abspath(target_path)
        self.top_path = self.current_path
        if current_state == 'repo':
            self.top_path = os.path.dirname(self.current_path)
        
        # Setup some helper objects and default information/variables
        self.current_state = current_state
        self.default_editor = None
        self.metadata_manager = PyAutogitMetadataManager(self)
        self.loaded_metadata = self.metadata_manager.read_metadata()
        self.credentials = credentials
        self.post_input_callback = None

        # Add a run on exit callback to save metadata
        if save_metadata:
            self.root.run_on_exit(self.metadata_manager.write_metadata)

        self.user_message = None

        self.operation_thread = None

        # Repository select screen widgets, key commands.
        self.repos = find_repos_in_path(self.top_path)

        self.repo_select_widget_set = py_cui.widget_set.WidgetSet(5,4)
        
        logo_label = self.repo_select_widget_set.add_block_label(self.get_logo_text(), 0, 0, column_span=2, center=False)
        logo_label.set_standard_color(py_cui.MAGENTA_ON_BLACK)

        link_label = self.repo_select_widget_set.add_label('v{} - https://github.com/jwlodek/pyautogit'.format(__version__), 0, 2, column_span=2)
        link_label.add_text_color_rule('https://.*', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')
        
        self.repo_menu = self.repo_select_widget_set.add_scroll_menu('Repositories in Workspace', 1, 2, row_span=2)
        self.repo_menu.add_item_list(self.repos)
        self.repo_menu.add_key_command(py_cui.keys.KEY_ENTER,   self.open_autogit_window)
        self.repo_menu.add_key_command(py_cui.keys.KEY_SPACE,   self.repo_select_manager.show_repo_status)
        self.repo_menu.add_key_command(py_cui.keys.KEY_DELETE,  self.repo_select_manager.ask_delete_repo)

        self.git_status_box = self.repo_select_widget_set.add_text_block('Git Repo Status', 1, 0, row_span=4, column_span=2)
        self.git_status_box.is_selectable = False
        self.git_status_box.add_text_color_rule('Welcome', py_cui.GREEN_ON_BLACK, 'startswith', match_type='line')
        
        self.current_status_box = self.repo_select_widget_set.add_text_block('Current Status', 1, 3, row_span=2)
        self.current_status_box.is_selectable = False
        
        self.clone_new_box = self.repo_select_widget_set.add_text_box('Clone Repository - Enter Remote URL', 3, 2, column_span=2)
        self.clone_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : self.repo_select_manager.execute_long_operation('Cloning', self.repo_select_manager.clone_new_repo, credentials_required=True))
        
        self.create_new_box = self.repo_select_widget_set.add_text_box('Create New Repository - Enter Directory Name', 4, 2, column_span=2)
        self.create_new_box.add_key_command(py_cui.keys.KEY_ENTER, self.repo_select_manager.create_new_repo)
        
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.repo_select_manager.refresh_git_status)
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, self.ask_credentials)
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.repo_select_manager.show_menu)
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_E_LOWER, self.ask_default_editor)
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, lambda : self.git_status_box.set_text(self.get_about_info()))
        self.repo_select_manager.refresh_git_status()
        
        if self.current_state == 'workspace':
            if self.metadata_manager.first_time:
                self.git_status_box.set_text(self.get_welcome_message())
                self.metadata_manager.first_time = False
            else:
                self.git_status_box.set_text(self.get_about_info(with_logo = False))
            self.metadata_manager.apply_metadata(self.loaded_metadata)
            self.root.set_title('pyautogit v{} - Repository Selection'.format(__version__))
            self.root.set_status_bar_text('Quit - q | Full Menu - m | Refresh - r | Update Credentials - c')
            self.root.apply_widget_set(self.repo_select_widget_set)


        # Repo Control window screen widgets, key commands.
        self.repo_control_widget_set = py_cui.widget_set.WidgetSet(9, 8)

        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.open_repo_select_window)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.repo_control_manager.refresh_git_status)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.repo_control_manager.show_menu)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_L_LOWER, self.repo_control_manager.show_log)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, self.repo_control_manager.add_all_changes)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_E_LOWER, self.repo_control_manager.open_editor)
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_F_LOWER, lambda : self.repo_control_manager.execute_long_operation('Pulling', self.repo_control_manager.pull_repo_branch, credentials_required=True))
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_P_LOWER, lambda : self.repo_control_manager.execute_long_operation('Pushing', self.repo_control_manager.push_repo_branch, credentials_required=True))
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_C_UPPER, self.repo_control_manager.ask_custom_command)

        self.add_files_menu = self.repo_control_widget_set.add_scroll_menu('Add Files', 0, 0, row_span=2, column_span=2)
        self.add_files_menu.add_text_color_rule(' ', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith',    match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.add_revert_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_SPACE, self.repo_control_manager.open_git_diff_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_E_LOWER, self.repo_control_manager.open_editor_file)
        self.add_files_menu.set_focus_text('Enter - git add | Space - see diff | Arrows - scroll | Esc - Return')

        self.remotes_menu = self.repo_control_widget_set.add_scroll_menu('Git Remotes', 2, 0, row_span=2, column_span=2)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.show_remote_info)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_DELETE, self.repo_control_manager.delete_remote)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_R_LOWER, lambda : self.ask_message('Please enter a new remote name', callback=self.repo_control_manager.rename_remote))
        self.remotes_menu.set_focus_text('Enter - Show Remote Info | Delete - Delete Remote | Esc - Return')

        self.branch_menu = self.repo_control_widget_set.add_scroll_menu('Git Branches', 4, 0, row_span=2, column_span=2)
        self.branch_menu.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.checkout_branch)
        self.branch_menu.add_key_command(py_cui.keys.KEY_SPACE, self.repo_control_manager.show_log)
        self.branch_menu.set_focus_text('Enter - Checkout Branch | Space - Print Info | Arrows - Scroll | Esc - Return')

        self.commits_menu = self.repo_control_widget_set.add_scroll_menu('Recent Commits', 6, 0, row_span=2, column_span=2)
        self.commits_menu.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.show_commit_info)
        self.commits_menu.add_key_command(py_cui.keys.KEY_SPACE, self.repo_control_manager.checkout_commit)
        self.commits_menu.add_text_color_rule('^.*? ', py_cui.GREEN_ON_BLACK, 'contains', match_type='regex', include_whitespace=True)
        self.commits_menu.set_focus_text('Enter - Show commit info | Space - Checkout commit | Esc - Return')

        self.info_text_block = self.repo_control_widget_set.add_text_block('Git Info', 0, 2, row_span=8, column_span=6)
        self.info_text_block.add_text_color_rule('+',           py_cui.GREEN_ON_BLACK,  'startswith')
        self.info_text_block.add_text_color_rule('-',           py_cui.RED_ON_BLACK,    'startswith')
        self.info_text_block.add_text_color_rule('commit',      py_cui.YELLOW_ON_BLACK, 'startswith')
        self.info_text_block.add_text_color_rule('Copyright',   py_cui.CYAN_ON_BLACK,   'startswith')
        self.info_text_block.add_text_color_rule('@.*@',        py_cui.CYAN_ON_BLACK,   'contains', match_type='regex')
        self.info_text_block.add_text_color_rule('**    ',      py_cui.RED_ON_BLACK,    'startswith')
        #self.info_text_block.selectable = False
        
        self.new_branch_textbox = self.repo_control_widget_set.add_text_box('New Branch', 8, 0, column_span=2)
        self.new_branch_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.create_new_branch)
        self.new_branch_textbox.set_focus_text('Enter - Create new branch | Esc - Return')
        
        self.commit_message_box = self.repo_control_widget_set.add_text_box('Commit Message', 8, 2, column_span=6)
        self.commit_message_box.add_key_command(py_cui.keys.KEY_ENTER, self.repo_control_manager.commit)
        self.commit_message_box.set_focus_text('Enter - Commit changes | Esc - Return')

        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, lambda : self.root.move_focus(self.commit_message_box))
        self.repo_control_widget_set.add_key_command(py_cui.keys.KEY_I_LOWER, lambda : self.info_text_block.set_text(get_about_info()))

        if self.current_state == 'repo':
            self.git_status_box.clear()
            self.metadata_manager.apply_metadata(self.loaded_metadata)
            self.info_text_block.set_text(self.get_about_info())
            self.root.apply_widget_set(self.repo_control_widget_set)
            self.root.set_title('pyautogit v{} - {}'.format(__version__, os.path.basename(os.getcwd())))
            self.root.set_status_bar_text('Return - Bcksp | Full Menu - m | Refresh - r | Add all - a | Git log - l | Open Editor - e | Pull Branch - f | Push Branch - p | Command - C')
            self.repo_control_manager.refresh_git_status()
            

        self.repo_control_manager.info_panel = self.info_text_block
        self.repo_select_manager.info_panel = self.git_status_box


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

        target = self.repo_menu.get()
        self.git_status_box.clear()
        self.info_text_block.set_text(self.get_about_info())
        self.root.apply_widget_set(self.repo_control_widget_set)
        os.chdir(target)
        self.root.set_title('pyautogit v{} - {}'.format(__version__, target))
        self.root.set_status_bar_text('Return - Bcksp | Full Menu - m | Refresh - r | Add all - a | Git log - l | Open Editor - e | Pull Branch - f | Push Branch - p')
        self.repo_control_manager.refresh_git_status()


    def open_repo_select_window(self):
        """Function that opens the repository select window.

        Fired when the backspace key is pressed in the repository control window
        """

        self.commit_message_box.clear()
        self.info_text_block.clear()
        self.info_text_block.title = 'Git Info'
        self.branch_menu.clear()
        self.commits_menu.clear()
        self.add_files_menu.clear()
        self.remotes_menu.clear()
        self.new_branch_textbox.clear()
        if self.metadata_manager.first_time:
            self.git_status_box.set_text(self.get_welcome_message())
            self.metadata_manager.first_time = False
        else:
            self.git_status_box.set_text(self.get_about_info(with_logo = False))
        self.root.apply_widget_set(self.repo_select_widget_set)
        os.chdir('..')
        self.root.set_title('pyautogit v{} - Repository Selection'.format(__version__))
        self.root.set_status_bar_text('Quit - q | Full Menu - m | Refresh - r | Update Credentials - c')
        self.repo_select_manager.refresh_git_status()


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
        self.repo_select_manager.refresh_git_status()
        if self.post_input_callback is not None:
            self.post_input_callback()
        self.post_input_callback = None


    def ask_password(self, user):
        """Function that opens popup and asks for password.

        Also writes username to credentials

        Parameters
        ----------
        user : str
            The user's username
        """

        self.credentials.append(user)
        self.root.show_text_box_popup("Please enter your git remote password", self.update_password, password=True)


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
        self.root.show_text_box_popup("Please enter your git remote username", self.ask_password)



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

        self.root.show_loading_icon_popup('Please Wait', title, callback = post_loading_callback)
        self.operation_thread = threading.Thread(target=long_operation_function)
        self.operation_thread.start()


    def update_default_editor(self, editor):
        """Function that sets the default editor

        Parameters
        ----------
        editor : str
            command line call to open the editor
        """

        self.default_editor = editor
        self.root.show_message_popup('Default Editor Changed', '{} editor will be used to open directories'.format(editor))
        self.repo_select_manager.refresh_git_status()


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

        logo =         "         _    _ _______ ____   _____ _____ _______\n" 
        logo = logo +  "    /\\  | |  | |__   __/ __ \\ / ____|_   _|__   __|\n"
        logo = logo +  "   /  \\ | |  | |  | | | |  | | |  __  | |    | |   \n"
        logo = logo +  "  / /\\ \\| |  | |  | | | |  | | | |_ | | |    | |   \n"
        logo = logo +  " / ____ \\ |__| |  | | | |__| | |__| |_| |_   | |   \n"
        logo = logo +  "/_/    \\_\\____/   |_|  \\____/ \\_____|_____|  |_|   \n"
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
        about_info = about_info + 'Copyright (c) 2019 Jakub Wlodek'
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

    return repos


def is_git_repo(path):
    """Simple function that checks if a given path is a git repository.
    
    Note that all it does is check for the .git folder

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
    parser.add_argument('-c', '--credentials', action='store_true', help='Allows user to enter credentials once when pyautogit is started.')
    parser.add_argument('-w', '--workspace', help='Pass a path to this argument to start pyautogit in a workspace not the current directory.')
    parser.add_argument('-n', '--nosavemetadata', action='store_true', help='Add this flag if you would like pyautogit to not save metadata between sessions.')
    args = vars(parser.parse_args())
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
                print('Path {} is not a directory.'.format(args['workspace']))
                exit()
        else:
            print('Path {} does not exist.'.format(args['workspace']))
            exit()

    return target_repo, not args['nosavemetadata'], credentials


def main():
    """Entry point for pyautogit. Parses arguments, and initializes the CUI
    """

    target, save_metadata, credentials = parse_args()

    input_type = 'repo'
    if not is_git_repo(target):
        input_type = 'workspace'

    root = py_cui.PyCUI(5, 4)
    manager = PyAutogitManager(root, target, input_type, save_metadata, credentials)

    root.start()
