"""Manager implementation for CUI screen for selecting different repositories.
"""

import py_cui
import pyautogit
import pyautogit.commands
import pyautogit.screen_manager


class RepoSelectManager(pyautogit.screen_manager.ScreenManager):
    """Class representing the manager for the repo select screen

    Attributes
    ----------
    menu_choices : list of str
        Overriden attribute from base class with expanded menu choices.

    Methods
    -------
    process_menu_selection()
        Override of base class, executes depending on menu selection
    refresh_status()
        Function that refreshes the repositories in the selection screen
    ask_delete_repo()
        Function that asks user for confirmation for repo deletion
    delete_repo()
        Function that deletes a repo
    show_repo_status()
        Function that displays git status info for current repo
    clone_new_repo()
        Function that clones new repo from given URL
    create_new_repo()
        Function that creates a new repo with a given name
    """

    def __init__(self, top_manager):
        """Constructor for repo select manager
        """
        
        super().__init__(top_manager)
        self.menu_choices = ['(Re)Enter Credentials',
                                'Open Directory',
                                'Clone New Repository',
                                'Create New Repository',
                                'Select Text Editor',
                                'Enter Custom Command',
                                'Exit']


    def process_menu_selection(self, selection):
        """Override of base class, executes depending on menu selection


        Parameters
        ----------
        selection : str
            The user's menu selection
        """

        if selection == '(Re)Enter Credentials':
            self.manager.ask_credentials()
        elif selection == 'Open Directory':
            # This will be implemented once py_cui adds a filemanager popup.
            self.manager.open_not_supported_popup(selection)
            pass
        elif selection == 'Clone New Repository':
            self.manager.root.move_focus(self.manager.clone_new_box)
        elif selection == 'Create New Repository':
            self.manager.root.move_focus(self.manager.create_new_box)
        elif selection == 'Select Text Editor':
            self.manager.ask_default_editor()
        elif selection == 'Enter Custom Command':
            self.ask_custom_command()
        elif selection == 'Exit':
            exit()
        else:
            self.manager.open_not_supported_popup(selection)


    def initialize_screen_elements(self):
        repo_select_widget_set = py_cui.widget_set.WidgetSet(5,4)
        
        logo_label = repo_select_widget_set.add_block_label(self.manager.get_logo_text(), 0, 0, column_span=2, center=False)
        logo_label.set_standard_color(py_cui.MAGENTA_ON_BLACK)

        link_label = repo_select_widget_set.add_label('v{} - https://github.com/jwlodek/pyautogit'.format(pyautogit.__version__), 0, 2, column_span=2)
        link_label.add_text_color_rule('https://.*', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')
        
        self.repo_menu = repo_select_widget_set.add_scroll_menu('Repositories in Workspace', 1, 2, row_span=2)
        self.repo_menu.add_item_list(self.manager.repos)
        self.repo_menu.add_key_command(py_cui.keys.KEY_ENTER,   self.manager.open_autogit_window)
        self.repo_menu.add_key_command(py_cui.keys.KEY_SPACE,   self.show_repo_status)
        self.repo_menu.add_key_command(py_cui.keys.KEY_DELETE,  self.ask_delete_repo)

        self.git_status_box = repo_select_widget_set.add_text_block('Git Repo Status', 1, 0, row_span=4, column_span=2)
        self.git_status_box.is_selectable = False
        self.git_status_box.add_text_color_rule('Welcome', py_cui.GREEN_ON_BLACK, 'startswith', match_type='line')
        
        self.current_status_box = repo_select_widget_set.add_text_block('Current Status', 1, 3, row_span=2)
        self.current_status_box.is_selectable = False
        
        self.clone_new_box = repo_select_widget_set.add_text_box('Clone Repository - Enter Remote URL', 3, 2, column_span=2)
        self.clone_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : self.execute_long_operation('Cloning', self.clone_new_repo, credentials_required=True))
        
        self.create_new_box = repo_select_widget_set.add_text_box('Create New Repository - Enter Directory Name', 4, 2, column_span=2)
        self.create_new_box.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_repo)
        
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_S_LOWER, self.manager.open_settings_window)
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, self.manager.ask_credentials)
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_E_LOWER, self.manager.ask_default_editor)
        repo_select_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, lambda : self.git_status_box.set_text(self.manager.get_about_info()))
        
        self.refresh_status()
        return repo_select_widget_set

    
    def clear_elements(self):
        self.git_status_box.clear()


    def set_initial_values(self):
        if self.manager.metadata_manager.first_time:
            self.git_status_box.set_text(self.get_welcome_message())
            self.manger.metadata_manager.first_time = False
        else:
            self.git_status_box.set_text(self.manager.get_about_info(with_logo = False))
        self.manager.root.set_status_bar_text('Quit - q | Full Menu - m | Refresh - r | Update Credentials - c')


    def refresh_status(self):
        """Function that refreshes the repositories in the selection screen
        """

        self.manager.repos = pyautogit.find_repos_in_path(self.manager.workspace_path)
        self.repo_menu.clear()
        self.repo_menu.add_item_list(self.manager.repos)

        status_message = 'Current directory:\n{}\n\n'.format(self.manager.workspace_path)
        status_message = status_message + '# of Repos: {}\n\n'.format(len(self.manager.repos))
        if len(self.manager.credentials) == 0:
            status_message = status_message + 'Credentials Not Entered\n'
        else:
            status_message = status_message + 'Credentials Entered\n'
        if self.manager.default_editor is not None:
            status_message = status_message + '\nEditor: {}'.format(self.manager.default_editor)
        else:
            status_message = status_message + '\nNo Editor Specified.'
        self.current_status_box.set_text(status_message)


    def ask_delete_repo(self):
        """Function that asks user for confirmation for repo deletion
        """
        target = self.repo_menu.get()
        self.manager.root.show_yes_no_popup("Are you sure you want to delete {}?".format(target), self.delete_repo)


    def delete_repo(self, to_delete):
        """Function that deletes a repo

        Parameters
        ----------
        to_delete : bool
            User's response of request for confirmation of deletion
        """

        if to_delete:
            target = self.repo_menu.get()
            pyautogit.commands.remove_repo_tree(target)
            self.refresh_status()


    def show_repo_status(self):
        """Function that shows the current repository status
        """

        current_repo = self.repo_menu.selected_item
        repo_name = self.repo_menu.get()
        self.git_status_box.clear()
        out, err = pyautogit.commands.git_status(repo_name)
        if err != 0:
            self.manager.root.show_error_popup('Unable to get git status!', out)
        self.git_status_box.title = 'Git Repo Status - {}'.format(repo_name)
        self.git_status_box.set_text('\n{}'.format(out))
        self.refresh_status()
        self.repo_menu.selected_item = current_repo


    def clone_new_repo(self):
        """Function that clones new repo from given URL
        """

        new_repo_url = self.clone_new_box.get()
        self.message, self.status = pyautogit.commands.git_clone_new_repo(new_repo_url, self.manager.credentials)
        self.refresh_status()
        # Turn off loading popup
        self.manager.root.stop_loading_popup()


    def create_new_repo(self):
        """Function that creates a new repo with a given name
        """

        new_dir_target = self.create_new_box.get()
        out, err = pyautogit.commands.git_init_new_repo(new_dir_target)
        if err != 0:
            self.manager.root.show_error_popup('Unable to create new repository!', out)
        else:
            self.manager.root.show_message_popup('Created new repository', out)
        self.create_new_box.clear()
        self.refresh_status()

