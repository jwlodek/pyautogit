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
    """Class responsible for managing functions for the repository control screen.

    This class contains functions that are used by pyautogit for individual repository control.
    It provides the interface between the CUI widgets for the repository control screen and
    the pyautogit.commands module.

    Attributes
    ----------
    manager : PyAutogitManager
        The master PyAutogitManager object
    message : str
        A helper attribute for sending messages between functions
    status : int
        A helper attribute for sending status codes between functions
    utility_var : obj
        A helper attribute for sending objects between functions
    menu_choices : list of str
        A list of menu choices accessible from the repository control menu

    Methods
    -------
    
    """

    def __init__(self, top_manager):
        """Constructor for the RepoControlManager class
        """
        self.manager = top_manager
        self.message = ''
        self.status = 0
        self.utility_var = None
        self.menu_choices = ['Re-Enter Credentials', 'Push Branch', 'Pull Branch', 'Add Remote', 'Add All', 'Stash All', 'Stash Pop', 'Open Repository in Editor', 'About']


    def process_menu_selection(self, selection):
        if selection == 'Add Remote':
            self.ask_new_remote_name()
        elif selection == 'Add All':
            self.add_all_changes()
        elif selection == 'Push Branch':
            self.push_repo_branch_cred()
        elif selection == 'Pull Branch':
            self.pull_repo_branch_cred()
        elif selection == 'Stash All':
            self.stash_all_changes_op()
        elif selection == 'Stash Pop':
            self.unstash_all_changes_op()
        elif selection == 'About':
            self.manager.info_text_block.set_text(self.manager.get_about_info())
        elif selection == 'Open Repository in Editor':
            self.open_editor()
        elif selection == 'Re-Enter Credentials':
            self.manager.ask_credentials()
        else:
            self.manager.root.show_warning_popup('Warning - Not supported', 'This menu item has not yet been implemented.')


    def show_command_result(self, out, err, show_on_success = True, command_name='Command', success_message='Success', error_message='Error'):
        show_in_box = False
        stripped_output = out.strip()
        if len(out.splitlines()) > 1:
            popup_message = "Check Info Box For {} Output".format(command_name)
            show_in_box = True
        else:
            popup_message = stripped_output
        if err != 0:
            self.manager.root.show_error_popup(error_message, popup_message)
        elif show_on_success:
            self.manager.root.show_message_popup(success_message, popup_message)
        if show_in_box and (err != 0 or show_on_success):
            box_out = out
            if err != 0:
                err_out = '\n'
                temp = out.splitlines()
                for line in temp:
                    err_out = err_out + '- ' + line + '\n'
                box_out = err_out
            self.manager.info_text_block.title = '{} Output'.format(command_name)
            self.manager.info_text_block.set_text(box_out)


    # TODO: Make this a lambda function
    def show_menu(self):
        self.manager.root.show_menu_popup('Full Control Menu', self.menu_choices, self.process_menu_selection)


    def refresh_git_status(self):
        """Function that refreshes a git repository status
        """

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
        self.show_command_result(out, err, show_on_success=False, command_name="Show Status", error_message="Failed to get status")
        self.manager.add_files_menu.clear()
        self.manager.add_files_menu.add_item_list(out.splitlines())


    def get_repo_remotes(self):
        out, err = pyautogit.commands.git_get_remotes()
        self.show_command_result(out, err, show_on_success=False, command_name="List Remotes", error_message='Cannot get git remotes')
        self.manager.remotes_menu.clear()
        self.manager.remotes_menu.add_item_list(out.splitlines())


    def get_repo_branches(self):
        out, err = pyautogit.commands.git_get_branches()
        self.show_command_result(out, err, show_on_success=False, command_name="List Branches", error_message='Cannot get git branches')
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


    def show_commit_info(self):
        if self.manager.commits_menu.get() is None:
            return
        commit_hash = self.manager.commits_menu.get().split(' ')[0]
        out, err = pyautogit.commands.git_get_commit_info(commit_hash)
        if err != 0:
            self.manager.root.show_error_popup('Failed to generate commit info', out)
        else:
            self.manager.info_text_block.clear()
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Commit info for {}'.format(commit_hash)


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


    def stash_all_changes_op(self):
        self.manager.perform_long_operation('Stashing', self.stash_all_changes, lambda : self.show_status_long_op(name="Stash Changes", succ_message="Stashed changes", err_message="Failed to stash changes"))

    def stash_all_changes(self):
        self.message, self.status = pyautogit.commands.git_stash_all()
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()

    def unstash_all_changes_op(self):
        self.manager.perform_long_operation('Stashing', self.stash_all_changes, lambda : self.show_status_long_op(name="Pop stash", succ_message="Unstashed changes", err_message="Failed to unstash changes"))

    def unstash_all_changes(self):
        self.message, self.status = pyautogit.commands.git_unstash_all()

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


    def open_editor(self, file=None):
        if self.manager.default_editor is None:
            self.manager.root.show_error_popup('Error', 'No default editor specified.')
        else:
            current_path = os.getcwd()
            if file is not None:
                current_path = os.path.join(current_path, file)
            out, err = pyautogit.commands.open_default_editor(self.manager.default_editor, current_path)
            if err != 0:
                self.manager.root.show_error_popup('Failed to open editor.', out)
            else:
                self.manager.root.show_message_popup('Opened {}'.format(current_path), 'Opened {} editor in external window'.format(self.manager.default_editor))


    def open_editor_file(self):
        filename = self.manager.add_files_menu.get()[3:]
        self.open_editor(file=filename)


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

    def add_remote(self, remote_url):

        remote_name = self.utility_var
        self.utility_var = None
        out, err = pyautogit.commands.git_add_remote(remote_name, remote_url)
        self.show_command_result(out, err, show_on_success=False, command_name="Add Remote", error_message="Failed to add remote")
        self.manager.remotes_menu.clear()
        self.refresh_git_status()


    def ask_new_remote_url(self, remote_name):
        self.utility_var = remote_name
        self.manager.root.show_text_box_popup('Please enter the new remote url.', self.add_remote)

    def ask_new_remote_name(self):
        self.manager.root.show_text_box_popup('Please enter the new remote name.', self.ask_new_remote_url)

    def pull_repo_branch_cred(self):
        if not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation('Pulling', self.pull_repo_branch, self.show_status_long_op))
        else:
            self.manager.perform_long_operation('Pulling', self.pull_repo_branch, self.show_status_long_op)


    def pull_repo_branch(self):
        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_pull_branch(branch, remote, self.manager.credentials)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def commit(self):
        commit_message = self.manager.commit_message_box.get()
        out, err = pyautogit.commands.git_commit_changes(commit_message)
        self.show_command_result(out, err, show_on_success=False, command_name='Commit', success_message='Commit Succeeded',error_message='Commit Failed')
        self.refresh_git_status()
        self.show_log()
        self.manager.commit_message_box.clear()



    def push_repo_branch_cred(self):
        if not self.manager.were_credentials_entered():
            self.manager.ask_credentials(callback=lambda : self.manager.perform_long_operation('Pushing', self.push_repo_branch, self.show_status_long_op))
        else:
            self.manager.perform_long_operation('Pushing', self.push_repo_branch, self.show_status_long_op)


    def push_repo_branch(self):
        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_push_to_branch(branch, remote, self.manager.credentials)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def show_status_long_op(self, name='Command', succ_message="Success", err_message = "Err"):
        self.show_command_result(self.message, self.status, command_name=name, success_message=succ_message, error_message=err_message)
        self.message = ''
        self.status = 0


    def create_new_branch(self):

        new_branch_name = self.manager.new_branch_textbox.get()
        if len(new_branch_name) == 0:
            self.manager.root.show_error_popup('ERROR - Illegal branchname', 'Please enter a valid branchname.')
        else:
            out, err = pyautogit.commands.git_create_new_branch(new_branch_name)
            if err != 0:
                self.manager.show_error_popup('Failed to create branch', out)
            self.manager.root.lose_focus()
            self.manager.new_branch_textbox.clear()
            self.refresh_git_status()


    def checkout_branch(self):
        branch = self.manager.branch_menu.get()
        if branch is not None:
            branch = branch[2:]
            out, err = pyautogit.commands.git_checkout_branch(branch)
            self.show_command_result(out, err, command_name='Branch Checkout', success_message='Checked Out Branch {}'.format(branch), error_message='Failed To Checkout Branch')
            self.refresh_git_status()

