"""
File containing functions used by the repository specific CUI screen.
This file is meant to handle the intermediate considerations between the 
CUI and the underlying git commands found in pyautogit.commands

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import os
import py_cui
import pyautogit
import pyautogit.commands

class RepoControlManager:

    def __init__(self, top_manager):
        self.manager = top_manager

    def refresh_git_status(self):

        remote = self.manager.remotes_menu.selected_item
        selected_file = self.manager.add_files_menu.selected_item

        self.get_repo_branches()
        self.get_repo_remotes()
        self.get_repo_status_short()
        self.get_recent_commits()

        if len(self.manager.remotes_menu.get_item_list()) > remote:
            self.manager.remotes_menu.selected_item = remote
        if len(self.manager.add_files_menu.get_item_list()) > selected_file:
            self.manager.add_files_menu.selected_item = selected_file


    def get_repo_status_short(self):
        out, err = pyautogit.commands.git_status_short()
        if err < 0:
            self.manager.root.show_error_popup('Cannot get git status', out)
        else:
            self.manager.add_files_menu.clear()
            self.manager.add_files_menu.add_item_list(out.splitlines())


    def get_repo_remotes(self):
        out, err = pyautogit.commands.git_get_remotes()
        if err < 0:
            self.manager.root.show_error_popup('Cannot get git remotes', out)
        else:
            self.manager.remotes_menu.clear()
            self.manager.remotes_menu.add_item_list(out.splitlines())


    def get_repo_branches(self):
        out, err = pyautogit.commands.git_get_branches()
        if err < 0:
            self.manager.root.show_error_popup('Cannot get git branches', out)
        else:
            self.manager.branch_menu.clear()
            self.manager.branch_menu.add_item_list(out.splitlines())
            selected_branch = 0
            for branch in self.manager.branch_menu.get_item_list():
                if branch.startswith('*'):
                    break
                selected_branch = selected_branch + 1
            self.manager.branch_menu.selected_item = selected_branch


    def show_remote_info(self):
        if self.manager.branch_menu.get() is None:
            return
        remote = self.manager.remotes_menu.get()
        out, err = pyautogit.commands.git_get_remote_info(remote)
        if err < 0:
            self.manager.root.show_error_popup('Cannot get remote info', out)
        else:
            self.manager.info_text_block.clear()
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = '{} remote info'.format(remote)


    def get_recent_commits(self):

        if self.manager.branch_menu.get() is None:
            return
        branch = self.manager.branch_menu.get()[2:]
        out, err = pyautogit.commands.git_get_recent_commits(branch)
        if err < 0:
            self.manager.root.show_error_popup('Cannot get recent commits', out)
        else:
            self.manager.commits_menu.clear()
            self.manager.commits_menu.add_item_list(out.splitlines())


    def checkout_branch(self):
        if self.manager.branch_menu.get() is None:
            return
        branch = self.manager.branch_menu.get()[2:]
        out, err = pyautogit.commands.git_checkout_branch(branch)
        if err < 0:
            self.manager.root.show_error_popup('Cannot checkout branch {}'.format(branch), out)



    def show_log(self):
        if self.manager.branch_menu.get() is None:
            return
        branch = self.manager.branch_menu.get()[2:]
        out, err = pyautogit.commands.git_log(branch)
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git log for branch {}.'.format(branch), out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git log'


    def open_git_diff(self):
        out, err = pyautogit.commands.git_diff()
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff repo.', out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git Diff'


    def open_git_diff_file(self):
        filename = self.manager.add_files_menu.get()[3:]
        out, err = pyautogit.commands.git_diff_file(filename)
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff for file {}.'.format(filename), out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git Diff - {}'.format(filename)


    def open_editor(self):
        if self.manager.default_editor is None:
            self.manager.root.show_error_popup('Error', 'No default editor specified.')
        else:
            current_path = os.getcwd()
            out, err = pyautogit.commands.open_default_editor(self.manager.default_editor, current_path)
            if err != 0:
                self.manager.root.show_error_popup('Failed to open editor.', out)
            else:
                self.manager.root.show_message_popup('Opened {}'.format(current_path), 'Opened {} editor in external window'.format(self.manager.default_editor))

    def add_all_changes(self):
        out, err = pyautogit.commands.git_add_all()
        if err != 0:
            self.manager.root.show_error_popup('Git Add Error', out)
        else:
            self.refresh_git_status()

    def add_revert_file(self):
        filename = self.manager.add_files_menu.get()
        if filename.startswith(' ') or filename.startswith('?'):
            out, err = pyautogit.commands.git_add_file(filename[3:])
        else:
            out, err = pyautogit.commands.git_reset_file(filename[3:])
        if err < 0:
            self.manager.root.show_error_popup('Cannot add/revert file {}'.format(filename), out)
        else:
            self.refresh_git_status()

    def pull_repo_branch_cred(self):
        if not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=self.pull_repo_branch)
        else:
            self.pull_repo_branch()


    def pull_repo_branch(self):
        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        out, err = pyautogit.commands.git_pull_branch(branch, remote, self.manager.credentials)
        if err != 0:
            self.manager.root.show_error_popup('Failed to pull from remote', out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git Pull Status - {} - {}'.format(remote, branch)
            self.manager.root.show_message_popup('Pulled branch', 'Successfully pulled branch {} from remote {}'.format(branch, remote))
        self.refresh_git_status()


    def commit(self):
        commit_message = self.manager.commit_message_box.get()
        out, err = pyautogit.commands.git_commit_changes(commit_message)
        if err != 0:
            self.manager.root.show_error_popup('Commit failed!', out)
        else:
            self.manager.root.show_message_popup('Success', 'Committed: {}'.format(commit_message))
            self.refresh_git_status()
            self.show_log()



    def push_repo_branch_cred(self):
        if not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation('Pushing', self.push_repo_branch))
        else:
            self.manager.perform_long_operation('Pushing', self.push_repo_branch)


    def push_repo_branch(self):
        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        out, err = pyautogit.commands.git_push_to_branch(branch, remote, self.manager.credentials)
        if err != 0:
            self.manager.root.show_error_popup('Unable to push to remote!', out)
        else:
            self.manager.root.show_message_popup('Pushed Successfully', out)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


