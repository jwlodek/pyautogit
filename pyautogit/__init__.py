"""
File containing entry point for pyautogit, as well as a top level class for managing the program.
It also contains some helper functions and argument parsing.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

from pyautogit import repo_select_screen
import argparse
import getpass
import os
import subprocess


__version__='0.0.1'


class PyAutoGitManager:

    def __init__(self, target_path, current_state, credentials):

        self.current_path = os.path.abspath(target_path)
        self.top_path = self.current_path
        self.current_state = current_state
        #if current_state == 'repo':
        #    self.top_path = os.path.
        self.credentials = credentials
        self.repos = find_repos_in_path(target_path)
        #self.autogit_cui = autogit.AutoGitCUI()
        self.repo_select_cui = repo_select_screen.RepoSelectCUI(self, self.top_path)

    def refresh(self):
        self.repos = find_repos_in_path(self.top_path)

    def start(self):
        if self.current_state == 'repo':
            self.autogit_cui.start()
        else:
            self.repo_select_cui.start()


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

    manager = PyAutoGitManager(target, in_type, credentials)

    manager.start()
