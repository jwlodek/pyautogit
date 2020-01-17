"""Manager implementation for CUI screen for selecting different repositories.
"""

import py_cui
import pyautogit
import pyautogit.commands
import pyautogit.screen_manager


class RepoSelectManager(pyautogit.screen_manager.ScreenManager):

    def __init__(self, top_manager):
        
        super().__init__(top_manager)
        self.menu_choices = ['(Re)Enter Credentials',
                                'Open Directory',
                                'Clone New Repository',
                                'Create New Repository',
                                'Select Text Editor',
                                'Enter Custom Command',
                                'Exit']


    def process_menu_selection(self, selection):
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
            self.manager.open_not_supported_popup(selection)
            pass
        elif selection == 'Exit':
            exit()
        else:
            self.manager.open_not_supported_popup(selection)


    def refresh_git_status(self):
        """Function that refreshes the repositories in the selection screen
        """

        self.manager.repos = pyautogit.find_repos_in_path(self.manager.top_path)
        self.manager.repo_menu.clear()
        self.manager.repo_menu.add_item_list(self.manager.repos)

        status_message = 'Current directory:\n{}\n\n'.format(self.manager.top_path)
        status_message = status_message + '# of Repos: {}\n\n'.format(len(self.manager.repos))
        if len(self.manager.credentials) == 0:
            status_message = status_message + 'Credentials Not Entered\n'
        else:
            status_message = status_message + 'Credentials Entered\n'
        if self.manager.default_editor is not None:
            status_message = status_message + '\nEditor: {}'.format(self.manager.default_editor)
        else:
            status_message = status_message + '\nNo Editor Specified.'
        self.manager.current_status_box.set_text(status_message)


    def ask_delete_repo(self):
        target = self.manager.repo_menu.get()
        self.manager.root.show_yes_no_popup("Are you sure you want to delete {}?".format(target), self.delete_repo)


    def delete_repo(self, to_delete):
        if to_delete:
            target = self.manager.repo_menu.get()
            pyautogit.commands.remove_repo_tree(target)
            self.manager.repo_menu.remove_selected_item()



    def show_repo_status(self):
        current_repo = self.manager.repo_menu.selected_item
        repo_name = self.manager.repo_menu.get()
        self.manager.git_status_box.clear()
        out, err = pyautogit.commands.git_status(repo_name)
        if err != 0:
            self.manager.root.show_error_popup('Unable to get git status!', out)
        self.manager.git_status_box.title = 'Git Repo Status - {}'.format(repo_name)
        self.manager.git_status_box.set_text('\n{}'.format(out))
        self.refresh_git_status()
        self.manager.repo_menu.selected_item = current_repo


    def clone_new_repo(self):
        new_repo_url = self.manager.clone_new_box.get()
        self.message, self.status = pyautogit.commands.git_clone_new_repo(new_repo_url, self.manager.credentials)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def create_new_repo(self):
        new_dir_target = self.manager.create_new_box.get()
        out, err = pyautogit.commands.git_init_new_repo(new_dir_target)
        if err != 0:
            self.manager.root.show_error_popup('Unable to create new repository!', out)
        else:
            self.manager.root.show_message_popup('Created new repository', out)
        self.manager.create_new_box.clear()
        self.refresh_git_status()

