"""
File contains a screen for listing available repos in pyautogit workspace.
"""

import py_cui
import pyautogit
import pyautogit.commands


class RepoSelectManager:

    def __init__(self, top_manager):
        self.manager = top_manager

    def ask_delete_repo(self):
        target = self.manager.repo_menu.get()
        self.manager.root.show_yes_no_popup("Are you sure you want to delete {}?".format(target), self.delete_repo)

    def delete_repo(self, to_delete):
        if to_delete:
            target = self.manager.repo_menu.get()
            pyautogit.commands.remove_repo_tree(target)
            self.manager.repo_menu.remove_selected_item()


    def update_status(self):
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


    def show_repo_status(self):
        current_repo = self.manager.repo_menu.selected_item
        repo_name = self.manager.repo_menu.get()
        self.manager.git_status_box.clear()
        out, err = pyautogit.commands.git_status(repo_name)
        if err != 0:
            self.manager.root.show_error_popup('Unable to get git status!', out)
        self.manager.git_status_box.title = 'Git Repo Status - {}'.format(repo_name)
        self.manager.git_status_box.set_text('\n{}'.format(out))
        self.manager.refresh_repos()
        self.manager.repo_menu.selected_item = current_repo


    def clone_new_repo_cred(self):
        if not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=self.clone_new_repo)
        else:
            self.clone_new_repo()


    def clone_new_repo(self):
        new_repo_url = self.manager.clone_new_box.get()
        out, err = pyautogit.commands.git_clone_new_repo(new_repo_url, self.manager.credentials)
        if err != 0:
            self.manager.root.show_error_popup('Unable to clone repository!', out)
        else:
            self.manager.root.show_message_popup('Cloned new repository', out)
        self.manager.git_status_box.set_text(out)
        self.manager.refresh_repos()


    def create_new_repo(self):
        new_dir_target = self.manager.create_new_box.get()
        out, err = pyautogit.commands.git_init_new_repo(new_dir_target)
        if err != 0:
            self.manager.root.show_error_popup('Unable to create new repository!', out)
        else:
            self.manager.root.show_message_popup('Created new repository', out)
        self.manager.create_new_box.clear()
        self.manager.refresh_repos()




