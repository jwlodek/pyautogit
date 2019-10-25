"""
File containing class for main pyautogit CUI screen, and all related functions.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import py_cui
import pyautogit
import pyautogit.commands

from subprocess import Popen, PIPE



def refresh_git_status(manager):

    remote = manager.remotes_menu.selected_item
    selected_file = manager.add_files_menu.selected_item

    get_repo_branches(manager)
    get_repo_remotes(manager)
    get_repo_status_short(manager)
    get_recent_commits(manager)

    if len(manager.remotes_menu.get_item_list()) > remote:
        manager.remotes_menu.selected_item = remote
    if len(manager.add_files_menu.get_item_list()) > selected_file:
        manager.add_files_menu.selected_item = selected_file


def get_repo_status_short(manager):
    out, err = pyautogit.commands.git_status_short()
    if err < 0:
        manager.root.show_error_popup('Cannot get git status', out)
    manager.add_files_menu.clear()
    manager.add_files_menu.add_item_list(out.splitlines())


def get_repo_remotes(manager):
    out, err = pyautogit.commands.git_get_remotes()
    if err < 0:
        manager.root.show_error_popup('Cannot get git remotes', out)
    manager.remotes_menu.clear()
    manager.remotes_menu.add_item_list(out.splitlines())


def get_repo_branches(manager):
    out, err = pyautogit.commands.git_get_branches()
    if err < 0:
        manager.root.show_error_popup('Cannot get git branches', out)
    manager.branch_menu.clear()
    manager.branch_menu.add_item_list(out.splitlines())
    selected_branch = 0
    for branch in manager.branch_menu.get_item_list():
        if branch.startswith('*'):
            break
        selected_branch = selected_branch + 1
    manager.branch_menu.selected_item = selected_branch


def get_recent_commits(manager):

    branch = manager.branch_menu.get()[2:]
    out, err = pyautogit.commands.git_get_recent_commits(branch)
    if err < 0:
        manager.root.show_error_popup('Cannot get recent commits', out)
    manager.commits_menu.clear()
    manager.commits_menu.add_item_list(out.splitlines())


def add_revert_file(manager):
    filename = manager.add_files_menu.get()
    out, err = pyautogit.commands.git_add_file(filename)
    if err < 0:
        manager.root.show_error_popup('Cannot add/revert file {}'.format(filename), out)


def checkout_branch(manager):
    branch = manager.branch_menu.get()
    out, err = pyautogit.commands.git_checkout_branch(branch)
    if err < 0:
        manager.root.show_error_popup('Cannot checkout branch {}'.format(branch), out)



def show_log(manager):
    branch = manager.branch_menu.get()
    out, err = pyautogit.commands.git_log(branch)
    if err < 0:
        manager.root.show_error_popup('Unable to show git log for branch {}.'.format(branch), out)
    else:
        manager.info_text_block.set_text(out)
        manager.info_text_block.title = 'Git log'


def open_git_diff(manager):
    out, err = pyautogit.commands.git_diff()
    if err < 0:
        manager.root.show_error_popup('Unable to show git diff repo.', out)
    else:
        manager.info_text_block.set_text(out)
        manager.info_text_block.title = 'Git Diff'


def open_git_diff_file(manager):
    filename = manager.add_files_menu.get()[3:]
    out, err = pyautogit.commands.git_diff_file(filename)
    if err < 0:
        manager.root.show_error_popup('Unable to show git diff for file {}.'.format(filename), out)
    else:
        manager.info_text_block.set_text(out)
        manager.info_text_block.title = 'Git Diff - {}'.format(filename)


def push_repo_branch_cred(manager):
    if not manager.were_credentials_entered():
        manager.ask_credentials(callback=lambda : push_repo_branch(manager))
    else:
        push_repo_branch(manager)


def push_repo_branch(manager):
    branch = manager.branch_menu.get()[2:]
    remote = manager.git_remotes_menu.get()
    out, err = pyautogit.commands.git_push_to_branch(branch, remote, manager.credentials)
    if err != 0:
        manager.root.show_error_popup('Unable to push to remote!', out)
    else:
        manager.root.show_message_popup('Pushed Successfully', out)
    manager.refresh_repos()