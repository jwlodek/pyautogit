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
import pyautogit.logger as LOGGER

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
    refresh_status()
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

        super().__init__(top_manager, 'repository control')
        self.menu_choices = ['(Re)Enter Credentials', 
                                'Push Branch', 
                                'Pull Branch', 
                                'Add Remote', 
                                'Add All', 
                                'Stash All', 
                                'Stash Pop',
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
        elif selection == 'Stash All':
            self.execute_long_operation('Stashing', self.stash_all_changes, credentials_required=False)
        elif selection == 'Stash Pop':
            self.execute_long_operation('Unstashing', self.unstash_all_changes, credentials_required=False)
        elif selection == 'Checkout Version':
            self.show_version_selection_screen()
        elif selection == 'About':
            self.info_panel.set_text(self.manager.get_about_info())
        elif selection == 'Open Repository in Editor':
            self.open_editor()
        elif selection == '(Re)Enter Credentials':
            self.manager.ask_credentials()
        elif selection == 'Enter Custom Command':
            self.ask_custom_command()
        elif selection == 'Exit':
            self.manager.close_cleanup()
            exit()
        else:
            self.manager.open_not_supported_popup(selection)


    def initialize_screen_elements(self):
        """Function that initializes the widgets for the repo control screen. Override of base class function

        Returns
        -------
        repo_control_widget_set : py_cui.widget_set.WidgetSet
            Widget set object for repo control screen
        """

        # Repo Control window screen widgets, key commands.
        repo_control_widget_set = py_cui.widget_set.WidgetSet(9, 8)

        # Base keyboard shortcuts.
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_repo_select_window)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_status)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_L_LOWER, self.show_log)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, self.add_all_changes)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_E_LOWER, self.open_editor)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_F_LOWER, lambda : self.execute_long_operation('Pulling', self.pull_repo_branch, credentials_required=True))
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_P_LOWER, lambda : self.execute_long_operation('Pushing', self.push_repo_branch, credentials_required=True))
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_overview)
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_C_UPPER, self.ask_custom_command)

        # Textboxes for commit message and new branch/tag
        self.new_branch_textbox = repo_control_widget_set.add_text_box('New Branch', 8, 0, column_span=2)
        self.new_branch_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_branch)
        self.new_branch_textbox.set_focus_text('Create New Branch - Enter | Help - h | Return - Esc')
        
        self.commit_message_box = repo_control_widget_set.add_text_box('Commit Message', 8, 2, column_span=6)
        self.commit_message_box.add_key_command(py_cui.keys.KEY_ENTER, self.commit)
        self.commit_message_box.set_focus_text('Commit Changes - Enter | Help - h | Return - Esc')

        # Add/Unstage files menu. Shows current git status
        self.add_files_menu = repo_control_widget_set.add_scroll_menu('Add Files', 0, 0, row_span=2, column_span=2)
        self.add_files_menu.add_text_color_rule(' ', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith',    match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_ENTER, self.add_revert_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_SPACE, self.open_git_diff_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_E_LOWER, self.open_editor_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_add_files_menu)
        self.add_files_menu.set_focus_text('Add/Unstage - Enter | Diff - Space | Edit - e | Help - h | Return - Esc')

        # Shows current git remotes
        self.remotes_menu = repo_control_widget_set.add_scroll_menu('Git Remotes', 2, 0, row_span=2, column_span=2)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_ENTER, self.show_remote_info)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_N_LOWER, self.ask_new_remote_name)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_DELETE, self.delete_remote)
        self.remotes_menu.add_key_command(py_cui.keys.KEY_R_LOWER, lambda : self.manager.ask_message('Please enter a new remote name', callback=self.rename_remote))
        self.remotes_menu.add_key_command(py_cui.keys.KEY_H_LOWER, self.show_help_remotes_menu)
        self.remotes_menu.set_focus_text('Remote Info - Enter | New Remote - n | Delete Remote - Delete | Help - h | Return - Esc')

        # Shows current git branches/tags
        self.branch_menu_state = 'branches'
        self.branch_menu = repo_control_widget_set.add_scroll_menu('Git Branches', 4, 0, row_span=2, column_span=2)
        self.branch_menu.add_key_command(py_cui.keys.KEY_ENTER,     self.checkout_branch)
        self.branch_menu.add_key_command(py_cui.keys.KEY_SPACE,     self.show_log)
        self.branch_menu.add_key_command(py_cui.keys.KEY_TAB,       self.show_tree)
        self.branch_menu.add_key_command(py_cui.keys.KEY_N_LOWER,   lambda : self.manager.root.move_focus(self.new_branch_textbox))
        self.branch_menu.add_key_command(py_cui.keys.KEY_T_LOWER,   self.show_tags)
        self.branch_menu.add_key_command(py_cui.keys.KEY_B_LOWER,   self.show_branches)
        self.branch_menu.add_key_command(py_cui.keys.KEY_M_LOWER,   self.merge_branches)
        self.branch_menu.add_key_command(py_cui.keys.KEY_U_LOWER,   self.revert_merge)
        self.branch_menu.add_key_command(py_cui.keys.KEY_H_LOWER,   self.show_help_branch_menu)
        self.branch_menu.add_key_command(py_cui.keys.KEY_DELETE,    self.delete_branch)
        self.branch_menu.set_focus_text('Checkout - Enter | Log - Space | New - n | Merge - m | Show Tags - t | Show Branches - b | Revert Merge - u | Help - h | Esc - Return')

        # Shows list of recent git commits for checked out branch.
        self.commits_menu = repo_control_widget_set.add_scroll_menu('Recent Commits', 6, 0, row_span=2, column_span=2)
        self.commits_menu.add_key_command(py_cui.keys.KEY_ENTER, self.show_commit_info)
        self.commits_menu.add_key_command(py_cui.keys.KEY_SPACE, self.checkout_commit)
        self.commits_menu.add_key_command(py_cui.keys.KEY_H_LOWER,   self.show_help_commits_menu)
        self.commits_menu.add_text_color_rule('^.*? ', py_cui.GREEN_ON_BLACK, 'contains', match_type='regex', include_whitespace=True)
        self.commits_menu.set_focus_text('Commit Info - Enter | Checkout - Space | Help - h | Return - Esc')

        # Main info text block listing information for all pyautogit operations
        self.info_text_block = repo_control_widget_set.add_text_block('Git Info', 0, 2, row_span=8, column_span=6)
        self.info_text_block.add_text_color_rule('+',           py_cui.GREEN_ON_BLACK,  'startswith')
        self.info_text_block.add_text_color_rule('-',           py_cui.RED_ON_BLACK,    'startswith')
        self.info_text_block.add_text_color_rule('commit',      py_cui.YELLOW_ON_BLACK, 'startswith')
        self.info_text_block.add_text_color_rule('Copyright',   py_cui.CYAN_ON_BLACK,   'startswith')
        self.info_text_block.add_text_color_rule('@.*@',        py_cui.CYAN_ON_BLACK,   'contains', match_type='regex')
        self.info_text_block.add_text_color_rule('**    ',      py_cui.RED_ON_BLACK,    'startswith')
        self.info_text_block.add_text_color_rule('\* *\w+ ',       py_cui.CYAN_ON_BLACK,   'contains', match_type='regex')
        #self.info_text_block.selectable = False

        # Add some simple shortcut commands
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, lambda : self.manager.root.move_focus(self.commit_message_box))
        repo_control_widget_set.add_key_command(py_cui.keys.KEY_I_LOWER, lambda : self.info_text_block.set_text(self.manager.get_about_info()))

        self.info_panel = self.info_text_block
        return repo_control_widget_set


    def clear_elements(self):
        """Function that clears elements of repo control window
        """

        self.commit_message_box.clear()
        self.info_text_block.clear()
        self.info_text_block.title = 'Git Info'
        self.branch_menu.clear()
        self.commits_menu.clear()
        self.add_files_menu.clear()
        self.remotes_menu.clear()
        self.new_branch_textbox.clear()


    def set_initial_values(self):
        """Function that initializes status bar and info text for repo control window
        """

        self.info_text_block.set_text(self.manager.get_about_info())
        self.branch_menu_state = 'branches'
        self.manager.root.set_status_bar_text('Return - Bcksp | Menu - m | Refresh - r | Add All - a | Commit - c | Log - l | Editor - e | Pull - f | Push - p')


    def refresh_status(self):
        """Function that refreshes a git repository status
        """

        remote = self.remotes_menu.selected_item
        selected_file = self.add_files_menu.selected_item

        if self.branch_menu_state == 'branches':
            self.get_repo_branches()
            self.branch_menu.title = 'Git Branches'
            self.new_branch_textbox.title = 'New Branch'
            self.new_branch_textbox.key_commands[py_cui.keys.KEY_ENTER] = self.create_new_branch
            self.new_branch_textbox.set_focus_text('Enter - Create new branch | Esc - Return')
        else:
            self.get_repo_tags()
            self.branch_menu.title = 'Git Tags'
            self.new_branch_textbox.title = 'New Tag'
            self.new_branch_textbox.key_commands[py_cui.keys.KEY_ENTER] = self.create_new_tag
            self.new_branch_textbox.set_focus_text('Enter - Create new tag | Esc - Return')
        
        self.get_repo_remotes()
        self.get_repo_status_short()
        self.get_recent_commits()

        if len(self.remotes_menu.get_item_list()) > remote:
            self.remotes_menu.selected_item = remote
        if len(self.add_files_menu.get_item_list()) > selected_file:
            self.add_files_menu.selected_item = selected_file


    def get_repo_status_short(self):
        """Gets shorthand repository status
        """

        out, err = pyautogit.commands.git_status_short()
        self.show_command_result(out, err, show_on_success=False, command_name="Show Status", error_message="Failed to get status")
        self.add_files_menu.clear()
        self.add_files_menu.add_item_list(out.splitlines())


    def get_repo_remotes(self):
        """Gets list of repository remotes
        """

        out, err = pyautogit.commands.git_get_remotes()
        self.show_command_result(out, err, show_on_success=False, command_name="List Remotes", error_message='Cannot get git remotes')
        self.remotes_menu.clear()
        self.remotes_menu.add_item_list(out.splitlines())


    def show_branches(self):
        """Function that swaps to showing branches
        """

        self.branch_menu_state = 'branches'
        self.refresh_status()


    def get_repo_branches(self):
        """Gets list of repository branches
        """

        out, err = pyautogit.commands.git_get_branches()
        self.show_command_result(out, err, show_on_success=False, command_name="List Branches", error_message='Cannot get git branches')
        self.branch_menu.clear()
        self.branch_menu.add_item_list(out.splitlines())
        selected_branch = 0
        for branch in self.branch_menu.get_item_list():
            if branch.startswith('*'):
                break
            selected_branch = selected_branch + 1
        self.branch_menu.selected_item = selected_branch


    def show_tags(self):
        """Function that swaps to showing tags
        """
        
        self.branch_menu_state = 'tags'
        self.refresh_status()


    def get_repo_tags(self):
        """Gets list of repository tags
        """

        out, err = pyautogit.commands.git_get_tags()
        self.show_command_result(out, err, show_on_success=False, command_name="List Tags", error_message="Cannot list git tags")
        self.branch_menu.clear()
        tags = out.splitlines()
        tags.reverse()
        self.branch_menu.add_item_list(tags)


    def show_remote_info(self):
        """Gets info about remote
        """

        if self.branch_menu.get() is None:
            return
        remote = self.remotes_menu.get()
        out, err = pyautogit.commands.git_get_remote_info(remote)
        if err < 0:
            self.manager.root.show_error_popup('Cannot get remote info', out)
        else:
            self.info_text_block.clear()
            self.info_text_block.set_text(out)
            self.info_text_block.title = '{} remote info'.format(remote)


    def show_commit_info(self):
        """Gets info about a particular commit
        """

        if self.commits_menu.get() is None:
            return
        commit_hash = self.commits_menu.get().split(' ', 1)[0]
        out, err = pyautogit.commands.git_get_commit_info(commit_hash)
        if err != 0:
            self.manager.root.show_error_popup('Failed to generate commit info', out)
        else:
            self.info_text_block.clear()
            self.info_text_block.set_text(out)
            self.info_text_block.title = 'Commit info for {}'.format(commit_hash)


    def get_recent_commits(self):
        """Gets list of recent commits to branch
        """

        if self.branch_menu.get() is None:
            return
        if self.branch_menu_state == 'branches':
            branch = self.branch_menu.get()[2:]
            if branch.startswith('(HEAD'):
                branch = branch.split(' ')[-1][:-1]
        else:
            branch = self.branch_menu.get()
        out, err = pyautogit.commands.git_get_recent_commits(branch)
        if err < 0:
            self.root.show_error_popup('Cannot get recent commits', out)
        else:
            self.commits_menu.clear()
            self.commits_menu.add_item_list(out.splitlines())


    def create_new_tag(self):
        """Creates a new tag
        """

        new_tag_name = self.new_branch_textbox.get()
        if new_tag_name is not None and len(new_tag_name) > 0:
            out, err = pyautogit.commands.git_create_tag(new_tag_name)
            self.show_command_result(out, err, command_name='Create Tag', success_message='Tag {} Created'.format(new_tag_name), error_message='Failed to Create Tag')
            self.show_log()
            self.show_tags()
            self.refresh_status()
        else:
            self.manager.show_warning_popup('Warning', 'Cannot create tag with an empty name!')


    def show_log(self):
        """Displays the git log
        """

        if self.branch_menu.get() is None:
            return
        if self.branch_menu_state == 'branches':
            branch = self.branch_menu.get()[2:]
            if branch.startswith('(HEAD'):
                branch = branch.split(' ')[-1][:-1]
        else:
            branch = self.branch_menu.get()
        out, err = pyautogit.commands.git_log(branch)
        if err < 0:
            self.root.show_error_popup('Unable to show git log for branch {}.'.format(branch), out)
        else:
            self.info_text_block.set_text(out)
            self.info_text_block.title = 'Git log'


    def show_tree(self):
        """Displays git log as a tree
        """

        if self.branch_menu.get() is None:
            return
        if self.branch_menu_state == 'branches':
            branch = self.branch_menu.get()[2:]
            if branch.startswith('(HEAD'):
                branch = branch.split(' ')[-1][:-1]
        else:
            branch = self.branch_menu.get()
        out, err = pyautogit.commands.git_tree(branch)
        if err < 0:
            self.root.show_error_popup('Unable to show git log for branch {}.'.format(branch), out)
        else:
            self.info_text_block.set_text(out)
            self.info_text_block.title = 'Git tree'


    def stash_all_changes(self):
        """Stashes all repo changes
        """

        self.message, self.status = pyautogit.commands.git_stash_all()
        self.refresh_status()
        self.manager.root.stop_loading_popup()


    def unstash_all_changes(self):
        """Pops the stash
        """

        self.message, self.status = pyautogit.commands.git_unstash_all()
        self.refresh_status()
        self.manager.root.stop_loading_popup()


    def open_git_diff(self):
        """Opens current git diff state
        """

        out, err = pyautogit.commands.git_diff()
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff repo.', out)
        else:
            self.info_text_block.set_text(out)
            self.info_text_block.title = 'Git Diff'


    def open_git_diff_file(self):
        """Gets the diff for a selected file
        """

        filename = self.add_files_menu.get()[3:]
        out, err = pyautogit.commands.git_diff_file(filename)
        if err < 0:
            self.manager.root.show_error_popup('Unable to show git diff for file {}.'.format(filename), out)
        else:
            self.info_text_block.set_text(out)
            self.info_text_block.title = 'Git Diff - {}'.format(filename)


    def open_editor(self, file=None):
        """Opens an external editor if selected
        """

        if self.manager.editor_type == 'Internal':
            self.manager.open_editor_window()
        elif self.manager.default_editor is None:
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

        filename = self.add_files_menu.get()[3:]
        self.open_editor(file=filename)


    def add_all_changes(self):
        """Adds all changes to staging
        """

        out, err = pyautogit.commands.git_add_all()
        if err != 0:
            self.manager.root.show_error_popup('Git Add Error', out)
        else:
            self.refresh_status()


    def add_revert_file(self):
        """Adds/Reverts single file from staging
        """

        filename = self.add_files_menu.get()
        if filename.startswith(' ') or filename.startswith('?'):
            out, err = pyautogit.commands.git_add_file(filename[3:])
        else:
            out, err = pyautogit.commands.git_reset_file(filename[3:])
        if err < 0:
            self.manager.root.show_error_popup('Cannot add/revert file {}'.format(filename), out)
        else:
            self.refresh_status()


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
        self.remotes_menu.clear()
        self.refresh_status()


    def delete_remote(self):
        """Deletes selected remote from local repo
        """

        remote = self.remotes_menu.get()
        out, err = pyautogit.commands.git_remove_remote(remote)
        self.show_command_result(out, err, show_on_success=False, command_name="Remove Remote", error_message="Failed to remove remote")
        self.remotes_menu.clear()
        self.refresh_status()


    def rename_remote(self):
        """Renames selected remote from local repo
        """

        new_name = self.manager.user_message
        remote = self.remotes_menu.get()
        out, err = pyautogit.commands.git_rename_remote(remote, new_name)
        self.show_command_result(out, err, show_on_success=False, command_name="Rename Remote", error_message="Failed to rename remote")
        self.remotes_menu.clear()
        self.refresh_status()


    def commit(self):
        """Commits currently staged items
        """

        commit_message = self.commit_message_box.get()
        out, err = pyautogit.commands.git_commit_changes(commit_message)
        self.show_command_result('Commit: {}'.format(commit_message), err, command_name='Commit', success_message='Commit Succeeded', error_message='Commit Failed')
        self.refresh_status()
        self.show_commit_info()
        #self.show_log()
        self.commit_message_box.clear()


    def pull_repo_branch(self):
        """Pulls from remote
        """

        branch = self.branch_menu.get()[2:]
        remote = self.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_pull_branch(branch, remote, self.manager.credentials)
        self.refresh_status()
        self.manager.root.stop_loading_popup()


    def push_repo_branch(self):
        """Pushes to remote
        """

        branch = self.branch_menu.get()[2:]
        remote = self.remotes_menu.get()
        self.message, self.status = pyautogit.commands.git_push_to_branch(branch, remote, self.manager.credentials)
        if self.status == 0:
            self.message = 'Pushed {} to {} successfully.'.format(branch, remote)
        self.refresh_status()
        self.manager.root.stop_loading_popup()


    def create_new_branch(self):
        """Creates new branch for repository
        """

        new_branch_name = self.new_branch_textbox.get()
        if len(new_branch_name) == 0:
            self.manager.root.show_error_popup('ERROR - Illegal branchname', 'Please enter a valid branchname.')
        else:
            out, err = pyautogit.commands.git_create_new_branch(new_branch_name)
            if err != 0:
                self.manager.show_error_popup('Failed to create branch', out)
            self.manager.root.lose_focus()
            self.new_branch_textbox.clear()
            self.refresh_status()


    def delete_branch(self):
        """Deletes selected branch
        """

        branch_name = self.branch_menu.get()
        if branch_name.startswith('* '):
            self.manager.root.show_error_popup('ERROR - Branch Checked Out', 'You cannot delete the currently checked out branch!')
        elif self.branch_menu_state == 'tags':
            self.manager.root.show_error_popup('ERROR - Tag Menu Open', 'Please open branch menu to delete branches.')
        elif branch_name[2:].startswith('(HEAD'):
            self.manager.root.show_warning_popup('Warning', 'Cannot delete detached head!')
            return
        else:
            out, err = pyautogit.commands.git_delete_branch(branch_name[2:])
            self.show_command_result(out, err, command_name='Delete Branch', success_message='Deleted Branch {}'.format(branch_name[2:]), error_message='Failed To Delete Branch')
            self.refresh_status()


    def checkout_branch(self):
        """Checks out specified branch
        """

        branch = self.branch_menu.get()
        if branch.startswith('* '):
            self.manager.root.show_warning_popup('Warning', 'The selected branch is already checked out!')
            return
        if branch is not None and self.branch_menu_state == 'branches':
            branch = branch[2:]
            if branch.startswith('(HEAD'):
                self.manager.root.show_warning_popup('Warning', 'Cannot checkout detached head!')
                return
            out, err = pyautogit.commands.git_checkout_branch(branch)
            self.show_command_result(out, err, command_name='Branch Checkout', success_message='Checked Out Branch {}'.format(branch), error_message='Failed To Checkout Branch')
            self.refresh_status()
        elif branch is not None:
            out, err = pyautogit.commands.git_checkout_tag(branch)
            self.show_command_result(out, err, command_name='Tag Checkout', success_message='Checked Out Tag {}'.format(branch), error_message='Failed To Checkout Tag')
            self.show_branches()
            self.refresh_status()


    def merge_branches(self):
        """Merges selected branch into the currently checked out branch
        """
        
        merge_branch = self.branch_menu.get()
        checkout_branch = None
        for branch in self.branch_menu.get_item_list():
            if branch.startswith('* '):
                checkout_branch = branch
        if merge_branch is None or checkout_branch is None:
            self.manager.root.show_error_popup('No branches', 'The current repo has no branches to merge!')
        elif merge_branch[2:] == checkout_branch[2:]:
            self.manager.root.show_error_popup('Same branch', 'You cannot merge the same branch with itself!')
        else:
            merge_branch = merge_branch[2:]
            out, err = pyautogit.commands.git_merge_branches(merge_branch)
            self.refresh_status()
            self.show_command_result(out, err, command_name='Merging Branches', success_message='Merged With {}'.format(merge_branch), error_message='Failed To Merge Branch')


    def revert_merge(self):
        """Undos the merge that was just performed
        """

        out, err = pyautogit.commands.git_revert_branch_merge()
        self.show_command_result(out, err, command_name='Revert Merge')
        self.refresh_status()


    def checkout_commit(self):
        """Checks out specified commit
        """

        commit = self.commits_menu.get()
        if commit is not None:
            commit_hash = commit.split(' ', 1)[0]
            out, err = pyautogit.commands.git_checkout_commit(commit_hash)
            self.show_command_result(out, err, command_name='Commit Checkout', success_message='Checked Out Commit {}'.format(commit_hash), error_message='Failed To Checkout Commit')
            self.refresh_status()


    #-------------------------------------------------------#
    # HELP MESSAGE PRINT FUNCTIONS                          #
    #-------------------------------------------------------#


    def show_help_overview(self):
        """Function that displays help message for overview mode.
        """

        help_message = '\n'
        help_message = help_message + 'Welcome to the repository control screen.\nYou are currently in overview mode.\n'
        help_message = help_message + '\nIn overview mode, use the arrow keys to move between widgets.\nUse the Enter key to enter a menu or text field, and "m" to open a popup menu.\n'
        help_message = help_message + '\nTo return to the workspace screen, press Backspace.\nTo create a new commit, either use "a" to add all, or enter the add-files\n'
        help_message = help_message + 'menu to select individual files.\nThen, navigate to the commit message box to add a commit message.\n'
        help_message = help_message + 'You can automatically enter the commit message box from overview mode by pressing "c".\n'
        help_message = help_message + '\nIn addition, to refresh the window based on changes made outside of pyautogit, press "r".\n'
        help_message = help_message + '\nTo show help information for a specific submenu, enter it, and press "h".\n'
        self.info_text_block.title = 'Repo Control Overview Help'
        self.info_text_block.set_text(help_message)


    def show_help_add_files_menu(self):
        """Function that displays help message for the add files menu.
        """

        help_message = '\n'
        help_message = help_message + 'Your currently selected menu is the add files menu.\n'
        help_message = help_message + '\nFrom here, use the arrow keys to scroll, Enter to stage and unstage files for commit.\n'
        help_message = help_message + '\nIf you would like to edit a file, press "e".\nThis will open the internal editor or if specified an external one.\n'
        help_message = help_message + '\nPressing the Space button will display git diff information for the selected file, if any.\n'
        help_message = help_message + '\nTo return to overview mode, press Escape.\n'
        self.info_text_block.title = 'Add Files Menu Help'
        self.info_text_block.set_text(help_message)

    
    def show_help_remotes_menu(self):
        """Function that displays help message for the add files menu.
        """

        help_message = '\n'
        help_message = help_message + 'You have selected the remotes menu.\n\nFrom here, press Enter to show remote info, Delete to delete the remote,\n'
        help_message = help_message + '"n" to create a new remote, and Escape to return to overview mode.\n'
        self.info_text_block.title = 'Remotes Menu Help'
        self.info_text_block.set_text(help_message)


    def show_help_branch_menu(self):
        """Function that displays help message for the add files menu.
        """

        help_message = '\n'
        help_message = help_message + 'This is the branch/tags menu. Use this in combination with the below textbox to\n'
        help_message = help_message + 'control and create new branches or tags. To swap to seeing tags, press "t", and press "b"\n'
        help_message = help_message + 'to go back to viewing branches.\n'
        help_message = help_message + '\nTo create a new branch/tag, select the appropriate mode, and enter the name into the textbox.\n'
        help_message = help_message + '\nTo checkout a branch/tag select it and press enter.\nTo show a log or tree for the branch, press Space or Tab.\n'
        help_message = help_message + '\n To merge two branches together, checkout one and select another and press "m".\nThis will merge the selected one into the checked out one.\n'
        help_message = help_message + '\nTo return to overview mode, press Escape.\n'
        self.info_text_block.title = 'Branch/Tag Menu Help'
        self.info_text_block.set_text(help_message)


    def show_help_commits_menu(self):
        """Function that displays help message for the add files menu.
        """

        help_message = '\n'
        help_message = help_message + 'This is the commits menu. You can check out individual commits and show commit info.\n'
        help_message = help_message + '\nTo check out a commit, select it and press Space, to show info, select and press Enter\n'
        help_message = help_message + '\nTo return to overview mode, press Escape.\n'
        self.info_text_block.title = 'Commits Menu Help'
        self.info_text_block.set_text(help_message)
