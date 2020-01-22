"""File containing functions used by the repository specific CUI screen.

This file is meant to handle the intermediate considerations between the 
CUI and the underlying git commands found in pyautogit.commands

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import os
from sys import platform
import py_cui
import pyautogit
import pyautogit.commands
import pyautogit.screen_manager

class RepoControlManager(pyautogit.screen_manager.ScreenManager):
    """Class responsible for managing functions for the repository control screen.

    This class contains functions that are used by pyautogit for individual repository control.
    It provides the interface between the CUI widgets for the repository control screen and
    the pyautogit.commands module.

    Attributes
    ----------
    menu_choices : list of str
        Overriden list of menu choices accessible from the repository control menu

    Methods
    -------
    process_menu_selection()
        Override of base class, executes based on user menu selection
    refresh_git_status()
        Function that refreshes a git repository status
    get_repo_status_short()
        Gets shorthand repository status
    get_repo_remotes()
        gets list of repository remotes
    get_repo_branches()
        gets list of repository branches
    show_remote_info()
        gets info about remote
    show_commit_info()
        gets info about a particular commit
    get_recent_commits()
        gets list of recent commits to branch
    create_new_tag()
        Creates a new tag
    show_log()
        Displays the git log
    stash_all_changes()
        Stashes all repo changes
    unstash_all_changes()
        Pops the stash
    open_git_diff()
        Opens current git diff state
    open_git_diff_file()
        Gets the diff for a selected file
    open_editor()
        Opens an external editor if selected
    open_editor_file()
        Opens an external editor for a selected file
    add_all_changes()
        Adds all changes to staging
    add_revert_file
        Adds/Reverts single file from staging
    ask_new_remote_name()
        Asks user for new remote name
    ask_new_remote_url()
        Asks user for new remote url
    add_remote()
        Adds a new remote to repo
    delete_remote()
        Deletes selected remote from local repo
    rename_remote()
        Renames selected remote from local repo
    commit()
        Commits currently staged items
    pull_repo_branch()
        pulls from remote
    push_repo_branch()
        pushes to remote
    create_new_branch()
        Creates new branch for repository
    checkout_branch()
        Checks out specified branch
    checkout_commit()
        Checks out specified commit
    """

    def __init__(self, top_manager):
        """Constructor for the RepoControlManager class
        """

        super().__init__(top_manager)
        self.menu_choices = ['(Re)Enter Credentials', 
                                'Push Branch', 
                                'Pull Branch', 
                                'Merge With Branch',
                                'Add Remote', 
                                'Add All', 
                                'Stash All', 
                                'Stash Pop', 
                                'Create Tag',
                                'Synchronize Tags',
                                'Checkout Version',
                                'Open Repository in Editor', 
                                'Enter Custom Command', 
                                'About',
                                'Exit']


    def process_menu_selection(self, selection):
        """Override of base class, executes based on user menu selection

        Parameters
        ----------
        selection : str
            User selection from menu
        """

        if selection == 'Add Remote':
            self.ask_new_remote_name()
        elif selection == 'Add All':
            self.add_all_changes()
        elif selection == 'Push Branch':
            self.execute_long_operation('Pushing', self.push_repo_branch, credentials_required=True)
        elif selection == 'Pull Branch':
            self.execute_long_operation('Pulling', self.pull_repo_branch, credentials_required=True)
        elif selection == 'Merge With Branch':
            #self.execute_long_operation('Merging', self.merge_branches, credentials_required=False)
            self.merge_branches()
        elif selection == 'Stash All':
            self.execute_long_operation('Stashing', self.stash_all_changes, credentials_required=False)
        elif selection == 'Stash Pop':
            self.execute_long_operation('Unstashing', self.unstash_all_changes, credentials_required=False)
        elif selection == 'Create Tag':
            self.manager.ask_message('Please enter your new git tag', callback=self.create_new_tag)
        elif selection == 'Checkout Version':
            self.show_version_selection_screen()
        elif selection == 'About':
            self.manager.info_text_block.set_text(self.manager.get_about_info())
        elif selection == 'Open Repository in Editor':
            self.open_editor()
        elif selection == 'Re-Enter Credentials':
            self.manager.ask_credentials()
        elif selection == 'Enter Custom Command':
            self.ask_custom_command()
        elif selection == 'Exit':
            exit()
        else:
            self.manager.open_not_supported_popup(selection)


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
        """Gets shorthand repository status
        """

        out, err = pyautogit.commands.git_status_short()
        self.show_command_result(out, err, show_on_success=False, command_name="Show Status", error_message="Failed to get status")
        self.manager.add_files_menu.clear()
        self.manager.add_files_menu.add_item_list(out.splitlines())


    def get_repo_remotes(self):
        """Gets list of repository remotes
        """

        out, err = pyautogit.commands.git_get_remotes()
        self.show_command_result(out, err, show_on_success=False, command_name="List Remotes", error_message='Cannot get git remotes')
        self.manager.remotes_menu.clear()
        self.manager.remotes_menu.add_item_list(out.splitlines())


    def get_repo_branches(self):
        """Gets list of repository branches
        """

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
        """Gets info about remote
        """

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
        """Gets info about a particular commit
        """

        if self.manager.commits_menu.get() is None:
            return
        commit_hash = self.manager.commits_menu.get().split(' ', 1)[0]
        out, err = pyautogit.commands.git_get_commit_info(commit_hash)
        if err != 0:
            self.manager.root.show_error_popup('Failed to generate commit info', out)
        else:
            self.manager.info_text_block.clear()
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Commit info for {}'.format(commit_hash)


    def get_recent_commits(self):
        """Gets list of recent commits to branch
        """

        if self.manager.branch_menu.get() is None:
            return
        branch = self.manager.branch_menu.get()[2:]
        if branch.startswith('(HEAD'):
            branch = branch.split(' ')[-1][:-1]
        out, err = pyautogit.commands.git_get_recent_commits(branch)
        if err < 0:
            self.manager.root.show_error_popup('Cannot get recent commits', out)
        else:
            self.manager.commits_menu.clear()
            self.manager.commits_menu.add_item_list(out.splitlines())


    def create_new_tag(self):
        """Creates a new tag
        """

        new_tag_name = self.manager.user_message
        out, err = pyautogit.commands.git_create_tag(new_tag_name)
        self.show_command_result(out, err, command_name='Create Tag', success_message='Tag {} Created'.format(new_tag_name), error_message='Failed to Create Tag')
        self.show_log()


    def show_log(self):
        """Displays the git log
        """

        if self.manager.branch_menu.get() is None:
            return
        branch = self.manager.branch_menu.get()[2:]
        out, err = pyautogit.commands.git_log(branch)
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git log for branch {}.'.format(branch), out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git log'


    def stash_all_changes(self):
        """Stashes all repo changes
        """

        self.message, self.status = pyautogit.commands.git_stash_all()
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def unstash_all_changes(self):
        """Pops the stash
        """

        self.message, self.status = pyautogit.commands.git_unstash_all()
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def open_git_diff(self):
        """Opens current git diff state
        """

        out, err = pyautogit.commands.git_diff()
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff repo.', out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git Diff'


    def open_git_diff_file(self):
        """Gets the diff for a selected file
        """

        filename = self.manager.add_files_menu.get()[3:]
        out, err = pyautogit.commands.git_diff_file(filename)
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff for file {}.'.format(filename), out)
        else:
            self.manager.info_text_block.set_text(out)
            self.manager.info_text_block.title = 'Git Diff - {}'.format(filename)


    def open_editor(self, file=None):
        """Opens an external editor if selected
        """

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
        """Opens an external editor for a selected file
        """

        filename = self.manager.add_files_menu.get()[3:]
        self.open_editor(file=filename)


    def add_all_changes(self):
        """Adds all changes to staging
        """

        out, err = pyautogit.commands.git_add_all()
        if err != 0:
            self.manager.root.show_error_popup('Git Add Error', out)
        else:
            self.refresh_git_status()


    def add_revert_file(self):
        """Adds/Reverts single file from staging
        """

        filename = self.manager.add_files_menu.get()
        if filename.startswith(' ') or filename.startswith('?'):
            out, err = pyautogit.commands.git_add_file(filename[3:])
        else:
            out, err = pyautogit.commands.git_reset_file(filename[3:])
        if err < 0:
            self.manager.root.show_error_popup('Cannot add/revert file {}'.format(filename), out)
        else:
            self.refresh_git_status()


    #-----------------------------------#
    #               REMOTES             #
    #-----------------------------------#


    def ask_new_remote_name(self):
        """Opens text box to enter new remote name
        """

        self.manager.root.show_text_box_popup('Please enter the new remote name.', self.ask_new_remote_url)


    def ask_new_remote_url(self, remote_name):
        """Opens text box to ask new remote url

        Parameters
        ----------
        remote_name : str
            Remote name entered in previous textbox
        """

        self.utility_var = remote_name
        self.manager.root.show_text_box_popup('Please enter the new remote url.', self.add_remote)


    def add_remote(self, remote_url):
        """Adds remote to git repo

        Parameters
        ----------
        remote_url : str
            URL entered by user
        """

        remote_name = self.utility_var
        self.utility_var = None
        out, err = pyautogit.commands.git_add_remote(remote_name, remote_url)
        self.show_command_result(out, err, show_on_success=False, command_name="Add Remote", error_message="Failed to add remote")
        self.manager.remotes_menu.clear()
        self.refresh_git_status()


    def delete_remote(self):
        """Deletes selected remote from local repo
        """

        remote = self.manager.remotes_menu.get()
        out, err = pyautogit.commands.git_remove_remote(remote)
        self.show_command_result(out, err, show_on_success=False, command_name="Remove Remote", error_message="Failed to remove remote")
        self.manager.remotes_menu.clear()
        self.refresh_git_status()


    def rename_remote(self):
        """Renames selected remote from local repo
        """

        new_name = self.manager.user_message
        remote = self.manager.remotes_menu.get()
        out, err = pyautogit.commands.git_rename_remote(remote, new_name)
        self.show_command_result(out, err, show_on_success=False, command_name="Rename Remote", error_message="Failed to rename remote")
        self.manager.remotes_menu.clear()
        self.refresh_git_status()


    def commit(self):
        """Commits currently staged items
        """

        commit_message = self.manager.commit_message_box.get()
        out, err = pyautogit.commands.git_commit_changes(commit_message)
        self.show_command_result('Commit: {}'.format(commit_message), err, command_name='Commit', success_message='Commit Succeeded', error_message='Commit Failed')
        self.refresh_git_status()
        self.show_commit_info()
        #self.show_log()
        self.manager.commit_message_box.clear()


    def pull_repo_branch(self):
        """Pulls from remote
        """

        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_pull_branch(branch, remote, self.manager.credentials)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()
    
    def push_repo_branch(self):
        """Pushes to remote
        """

        branch = self.manager.branch_menu.get()[2:]
        remote = self.manager.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_push_to_branch(branch, remote, self.manager.credentials)
        if self.status == 0:
            self.message = 'Pushed {} to {} successfully.'.format(branch, remote)
        self.refresh_git_status()
        self.manager.root.stop_loading_popup()


    def create_new_branch(self):
        """Creates new branch for repository
        """

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
        """Checks out specified branch
        """

        branch = self.manager.branch_menu.get()
        if branch is not None:
            branch = branch[2:]
            out, err = pyautogit.commands.git_checkout_branch(branch)
            self.show_command_result(out, err, command_name='Branch Checkout', success_message='Checked Out Branch {}'.format(branch), error_message='Failed To Checkout Branch')
            self.refresh_git_status()


    def merge_branches(self):
        """Merges selected branch into the currently checked out branch
        """
        
        merge_branch = self.manager.branch_menu.get()
        checkout_branch = None
        for branch in self.manager.branch_menu.get_item_list():
            if branch.startswith('* '):
                checkout_branch = branch
        if merge_branch is None or checkout_branch is None:
            self.manager.root.show_error_popup('No branches', 'The current repo has no branches to merge!')
        elif merge_branch[2:] == checkout_branch[2:]:
            self.manager.root.show_error_popup('Same branch', 'You cannot merge the same branch with itself!')
        else:
            out, err = pyautogit.commands.git_merge_branches(merge_branch)
            self.refresh_git_status()
            self.show_command_result(out, err, command_name='Merging Branches', success_message='Merged With {}'.format(merge_branch), error_message='Failed to Merge Branch')


    def revert_merge(self):
        """Undos the merge that was just performed
        """

        out, err = pyautogit.commands.git_revert_branch_merge()
        self.show_command_result(out, err, command_name='Revert Merge')
        self.refresh_git_status()


    def checkout_commit(self):
        """Checks out specified commit
        """

        commit = self.manager.commits_menu.get()
        if commit is not None:
            commit_hash = commit.split(' ', 1)[0]
            out, err = pyautogit.commands.git_checkout_commit(commit_hash)
            self.show_command_result(out, err, command_name='Commit Checkout', success_message='Checked Out Commit {}'.format(commit_hash), error_message='Failed To Checkout Commit')
            self.refresh_git_status()