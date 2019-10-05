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
        self.repos = find_repos_in_path(target_path)


        self.repo_select_widget_set = py_cui.widget_set.WidgetSet(5,4)
        self.repo_select_widget_set.add_block_label(get_logo_text(), 0, 0, column_span=2)
        self.repo_select_widget_set.add_label('v{} - https://github.com/jwlodek/pyautogit'.format(__version__), 0, 2, column_span=2)
        self.repo_menu = self.repo_select_widget_set.add_scroll_menu('Repositories in Workspace', 1, 2, row_span=2)
        self.repo_menu.add_item_list(self.repos)
        self.repo_menu.add_key_command(py_cui.keys.KEY_ENTER, lambda : RepoSelect.open_autogit_window(self))
        self.repo_menu.add_key_command(py_cui.keys.KEY_SPACE, lambda : RepoSelect.show_repo_status(self))
        self.git_status_box = self.repo_select_widget_set.add_text_block('Git Repo Status', 1, 0, row_span=4, column_span=2)
        self.git_status_box.is_selectable = False
        self.current_status_box = self.repo_select_widget_set.add_text_block('Current Status', 1, 3, row_span=2)
        self.current_status_box.is_selectable = False
        self.clone_new_box = self.repo_select_widget_set.add_text_box('Clone Repository - Enter Remote URL', 3, 2, column_span=2)
        self.clone_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : RepoSelect.clone_new_repo(self))
        self.create_new_box = self.repo_select_widget_set.add_text_box('Create New Repository - Enter Directory Name', 4, 2, column_span=2)
        self.create_new_box.add_key_command(py_cui.keys.KEY_ENTER, lambda : RepoSelect.create_new_repo(self))
        self.repo_select_widget_set.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_repos)
        RepoSelect.update_status(self)
        self.root.apply_widget_set(self.repo_select_widget_set)


        self.autogit_widget_set = py_cui.widget_set.WidgetSet(5, 5)
        #self.autogit_cui = autogit.AutoGitCUI()

    def refresh_repos(self):
        self.repos = find_repos_in_path(self.top_path)
        self.repo_menu.clear()
        self.repo_menu.add_item_list(self.repos)


def find_repos_in_path(path):
    repos = []
    for dir in os.listdir(path):
        new_dir = os.path.join(path, dir)
        if os.path.isdir(new_dir) and is_git_repo(new_dir):
            repos.append(os.path.basename(new_dir))

    return repos



def is_git_repo(path):
    is_repo = True
    FNULL = open(os.devnull, 'w')
    out = subprocess.call(['git', '-C', path, 'status'], stdout=FNULL, stderr=FNULL)
    if out != 0:
        is_repo = False
    FNULL.close()
    return is_repo


def parse_args():
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
    logo =         "        _    _ _______ ____   _____ _____ _______\n" 
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
