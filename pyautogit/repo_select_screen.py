"""
File contains a screen for listing available repos in pyautogit workspace.
"""

import pyautogit
import pyautogit.commands
import py_cui

class RepoSelectCUI:

    def __init__(self, manager, top_dir):
        self.root = py_cui.PyCUI(5, 4)
        self.manager = manager

        self.root.set_title('PyAutoGit v{} - Repo Select Screen'.format(pyautogit.__version__))

        self.root.add_block_label(pyautogit.get_logo_text(), 0, 0, column_span=2)
        self.root.add_label('v{} - https://github.com/jwlodek/pyautogit'.format(pyautogit.__version__), 0, 2, column_span=2)

        self.repo_menu = self.root.add_scroll_menu('Repositories in Workspace', 1, 2, row_span=2)
        self.repo_menu.add_item_list(self.manager.repos)
        self.repo_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_autogit_window)
        self.repo_menu.add_key_command(py_cui.keys.KEY_SPACE, self.show_repo_status)

        self.git_status_box = self.root.add_text_block('Git Repo Status', 1, 0, row_span=4, column_span=2)
        self.git_status_box.is_selectable = False

        self.current_status_box = self.root.add_text_block('Current Status', 1, 3, row_span=2)
        self.current_status_box.is_selectable = False

        self.clone_new_box = self.root.add_text_box('Clone Repository - Enter Remote URL', 3, 2, column_span=2)
        self.clone_new_box.add_key_command(py_cui.keys.KEY_ENTER, self.clone_new_repo)

        self.create_new_box = self.root.add_text_box('Create New Repository - Enter Directory Name', 4, 2, column_span=2)
        self.create_new_box.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_repo)

        self.root.add_key_binding(py_cui.keys.KEY_R_LOWER, self.manager.refresh)

        self.update_status()

    def update_status(self):
        status_message = 'Current workspace directory:\n{}\n\n'.format(self.manager.top_path)
        status_message = status_message + 'Current repos loaded in workspace: {}\n'.format(len(self.manager.repos))
        if len(self.manager.credentials) == 0:
            status_message = status_message + 'Git Remote Credentials Not Entered'
        else:
            status_messge = status_message + 'Git Remote Credentials Entered'
        self.current_status_box.set_text(status_message)

    def open_autogit_window(self):
        pass


    def show_repo_status(self):
        repo_name = self.repo_menu.get()
        self.git_status_box.clear()
        err, message = pyautogit.commands.git_status(repo_name)
        if err != 0:
            self.root.show_error_popup('Unable to get git status!', message)
        self.git_status_box.set_text(message)
        self.manager.refresh()


    def clone_new_repo(self):
        new_repo_url = self.clone_new_box.get()
        if len(self.manager.credentials) == 0:
            self.manager.ask_credentials(self)
        err, message = pyautogit.commands.git_clone_new_repo(new_repo_url, self.manager.credentials)
        if err != 0:
            self.root.show_error_popup('Unable to clone repository!', message)
        else:
            self.root.show_message_popup('Cloned new repository', message)
        self.manager.refresh()


    def create_new_repo(self):
        new_dir_target = self.create_new_box.get()
        err, message = pyautogit.commands.git_init_new_repo(new_dir_target)
        self.root.title='{}, {}'.format(err, message)
        if err != 0:
            self.root.show_error_popup('Unable to create new repository!', message)
        else:
            self.root.show_message_popup('Created new repository', message)
        self.create_new_box.clear()
        self.manager.refresh()


    def start(self):
        self.root.start()




