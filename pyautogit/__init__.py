"""
File containing entry point for pyautogit, as well as a top level class for managing the program.
It also contains some helper functions and argument parsing.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import argparse
import getpass
import os
import subprocess
from subprocess import Popen, PIPE

import py_cui

import pyautogit.repo_select_screen as RepoSelect
import pyautogit.autogit as Autogit


__version__='0.0.1'


class PyAutoGitManager:

    def __init__(self, root, target_path, current_state, credentials):

        self.root = root

        self.current_path = os.path.abspath(target_path)
        self.top_path = self.current_path
        self.current_state = current_state
        #if current_state == 'repo':
        #    self.top_path = os.path.
        self.credentials = credentials
        self.post_credential_callback = None

        # Repository select screen widgets, key commands.
        self.repos = find_repos_in_path(target_path)

        self.repo_select_widget_set = py_cui.widget_set.WidgetSet(5,4)
        self.repo_select_widget_set.add_block_label(get_logo_text(), 0, 0, column_span=2)
        self.repo_select_widget_set.add_label('v{} - https://github.com/jwlodek/pyautogit'.format(__version__), 0, 2, column_span=2)
        
        self.repo_menu = self.repo_select_widget_set.add_scroll_menu('Repositories in Workspace', 1, 2, row_span=2)
        self.repo_menu.add_item_list(self.repos)
        self.repo_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_autogit_window)
        self.repo_menu.add_key_command(py_cui.keys.KEY_SPACE, lambda : RepoSelect.show_repo_status(self))
        self.repo_menu.add_key_command(py_cui.keys.KEY_DELETE, lambda : RepoSelect.delete_repo(self))

        self.git_status_box = self.repo_select_widget_set.add_text_block('Git Repo Status', 1, 0, row_span=4, column_span=2)
        self.git_status_box.is_selectable = False
        
        self.current_status_box = self.repo_select_widget_set.add_text_block('Current Status', 1, 3, row_span=2)
        self.current_status_box.is_selectable = False
        
        self.clone_new_box = self.repo_select_widget_set.add_text_box('Clone Repository - Enter Remote URL', 3, 2, column_span=2)
        self.clone_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : RepoSelect.clone_new_repo_cred(self))
        
        self.create_new_box = self.repo_select_widget_set.add_text_box('Create New Repository - Enter Directory Name', 4, 2, column_span=2)
        self.create_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : RepoSelect.create_new_repo(self))
        
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_repos)
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_C_LOWER, self.ask_credentials)
        RepoSelect.update_status(self)
        self.root.apply_widget_set(self.repo_select_widget_set)


        # Autogit window screen widgets, key commands.
        self.autogit_widget_set = py_cui.widget_set.WidgetSet(9, 8)

        self.autogit_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.open_repo_select_window)
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_git_status)
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        self.autogit_widget_set.add_key_command(py_cui.keys.KEY_L_LOWER, lambda : Autogit.show_log(self))
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_A_LOWER, self.add_all)
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_E_LOWER, self.open_editor)
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_F_LOWER, self.fetch_branch)
        #self.autogit_widget_set.add_key_command(py_cui.keys.KEY_P_LOWER, self.push_branch)

        self.add_files_menu = self.autogit_widget_set.add_scroll_menu('Add Files', 0, 0, row_span=2, column_span=2)
        self.add_files_menu.add_text_color_rule(' ', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.RED_ON_BLACK,   'startswith',       match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith',    match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.GREEN_ON_BLACK, 'notstartswith',    match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_ENTER, Autogit.add_revert_file(self))
        self.add_files_menu.add_key_command(py_cui.keys.KEY_SPACE, Autogit.open_git_diff(self))
        self.add_files_menu.help_text = 'Enter - git add, Space - see diff, Arrows - scroll, Esc - exit'

        self.git_remotes_menu =self.autogit_widget_set.add_scroll_menu('Git Remotes', 2, 0, row_span=2, column_span=2)

        self.branch_menu = self.autogit_widget_set.add_scroll_menu('Git Branches', 4, 0, row_span=2, column_span=2)
        self.branch_menu.add_key_command(py_cui.keys.KEY_ENTER, Autogit.checkout_branch(self))
        self.branch_menu.add_key_command(py_cui.keys.KEY_SPACE, Autogit.show_log(self))

        self.git_commits_menu = self.autogit_widget_set.add_scroll_menu('Recent Commits', 6, 0, row_span=2, column_span=2)
        #self.git_commits_menu.add_key_command(py_cui.keys.KEY_ENTER, Autogit.show_git_commit_diff(self))
        self.git_commits_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith', match_type='region', region=[0,7], include_whitespace=True)

        self.diff_text_block = self.autogit_widget_set.add_text_block('Git Info', 0, 2, row_span=8, column_span=6)
        self.diff_text_block.add_text_color_rule('+',           py_cui.GREEN_ON_BLACK,  'startswith')
        self.diff_text_block.add_text_color_rule('-',           py_cui.RED_ON_BLACK,    'startswith')
        self.diff_text_block.add_text_color_rule('commit',      py_cui.YELLOW_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule('Copyright',   py_cui.CYAN_ON_BLACK,   'startswith')
        self.diff_text_block.add_text_color_rule('@.*@',        py_cui.CYAN_ON_BLACK,   'contains', match_type='regex')
        #self.diff_text_block.selectable = False
        self.diff_text_block.set_text(get_logo_text())
        
        self.new_branch_textbox = self.autogit_widget_set.add_text_box('New Branch', 8, 0, column_span=2)
        self.commit_message_box = self.autogit_widget_set.add_text_box('Commit Message', 8, 2, column_span=6)


        #self.git_remotes_menu.add_key_command(py_cui.keys.KEY_ENTER, self.show_remote_info)

        #self.new_branch_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_branch)
        #self.commit_message_box.add_key_command(py_cui.keys.KEY_ENTER, self.ask_to_commit)



    def refresh_repos(self):
        self.repos = find_repos_in_path(self.top_path)
        self.repo_menu.clear()
        self.repo_menu.add_item_list(self.repos)


    def open_autogit_window(self):
        target = self.repo_menu.get()
        self.root.apply_widget_set(self.autogit_widget_set)
        os.chdir(target)
        self.root.set_title('pyautogit v{} - {}'.format(__version__, target))
        self.root.set_status_bar_text('Quit - q | Full Menu - m | Refresh - r | Add all - a | Git log - l | Open Editor - e | Pull Branch - f | Push Branch - p')
        Autogit.refresh_git_status(self)

    def open_repo_select_window(self):
        self.root.apply_widget_set(self.repo_select_widget_set)
        os.chdir('..')
        self.root.set_title('pyautogit v{} - Repository Selection'.format(__version__))
        self.root.set_status_bar_text('Quit - q | Full Menu - m | Refresh - r | Update Credentials - c')
        RepoSelect.update_status(self)


    # Credential handler functions

    def update_password(self, passwd):
        """Function called once password is entered. 

        If necessary, fires the post_credential_callback function

        Parameters
        ----------
        passwd : str
            The user's password
        """

        self.credentials.append(passwd)
        if self.post_credential_callback is not None:
            self.post_credential_callback()
        self.post_credential_callback = None


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
        del self.credentials[:]
        if callback is not None:
            self.post_credential_callback = callback
        self.root.show_text_box_popup("Please enter your git remote username", self.ask_password)


    def were_credentials_entered(self):
        """Simple function for checking if credentials were entered

        Returns
        -------
        True if credentials found, otherwise false
        """

        return len(self.credentials) == 2


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
    True if .git exists, False otherwise
    """

    is_repo = False
    if os.path.exists(os.path.join(path, '.git')):
        is_repo = True
    return is_repo


def parse_args():
    """Function that parses user arguments for pyautogit
    """


    target_repo = '.'
    input_type = 'repo'
    credentials = []

    parser = argparse.ArgumentParser(description="A command line interface for git commands.")
    parser.add_argument('-t', '--targetdir', help='Target git repository or workspace directory.')
    parser.add_argument('-c', '--credentials', action='store_true', help='Allows user to enter credentials once when pyautogit is started.')
    args = vars(parser.parse_args())
    if args['credentials']:
        user = input('Please enter your github/gitlab username > ')
        credentials.append(user)
        passwd = getpass.getpass(prompt="Please enter your github/gitlab password > ")
        credentials.append(passwd)
    if args['targetdir'] is not None:
        if os.path.exists(target_repo) and os.path.isdir(args['targetdir']):
            target_repo = args['targetdir']

    if not is_git_repo(target_repo):
        input_type = 'workspace'

    return target_repo, input_type, credentials


def get_logo_text():
    logo =         "         _    _ _______ ____   _____ _____ _______\n" 
    logo = logo +  "    /\\  | |  | |__   __/ __ \\ / ____|_   _|__   __|\n"
    logo = logo +  "   /  \\ | |  | |  | | | |  | | |  __  | |    | |   \n"
    logo = logo +  "  / /\\ \\| |  | |  | | | |  | | | |_ | | |    | |   \n"
    logo = logo +  " / ____ \\ |__| |  | | | |__| | |__| |_| |_   | |   \n"
    logo = logo +  "/_/    \\_\\____/   |_|  \\____/ \\_____|_____|  |_|   \n"
    return logo


def main():
    """ Entry point for pyautogit. Parses arguments, and initializes the CUI """

    target, in_type, credentials = parse_args()

    root = py_cui.PyCUI(5, 4)
    manager = PyAutoGitManager(root, target, in_type, credentials)

    root.start()
