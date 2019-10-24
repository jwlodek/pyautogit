"""
File containing class for main pyautogit CUI screen, and all related functions.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import py_cui
import pyautogit
import pyautogit.commands



def refresh_git_status(manager):

    try:
        proc = Popen(['git', 'branch'], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode().splitlines()
        manager.branch_menu.clear()
        manager.branch_menu.add_item_list(out)
        selected_branch = 0
        for branch in manager.branch_menu.get_item_list():
            if branch.startswith('*'):
                break
            selected_branch = selected_branch + 1
        remote = manager.git_remotes_menu.selected_item
        proc = Popen(['git', 'remote'], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode().splitlines()
        manager.git_remotes_menu.clear()
        manager.git_remotes_menu.add_item_list(out)
        proc = Popen(['git', '--no-pager', 'log', manager.branch_menu.get()[2:], '--oneline'], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode().splitlines()
        manager.git_commits_menu.clear()
        manager.git_commits_menu.add_item_list(out)
        selected_file = manager.add_files_menu.selected_item
        proc = Popen(['git', 'status', '-s'], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode().splitlines()
        manager.add_files_menu.clear()
        manager.add_files_menu.add_item_list(out)
        if len(manager.branch_menu.get_item_list()) > selected_branch:
            manager.branch_menu.selected_item = selected_branch
        if len(manager.git_remotes_menu.get_item_list()) > remote:
            manager.git_remotes_menu.selected_item = remote
        if len(manager.add_files_menu.get_item_list()) > selected_file:
            manager.add_files_menu.selected_item = selected_file

    except:
        self.root.show_warning_popup('Git Failed', 'Unable to get git status, please check git installation')


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
        manager.diff_text_block.set_text(out)
        manager.diff_text_block.title = 'Git log'


def open_git_diff(manager):
    out, err = pyautogit.commands.git_diff()
    if err < 0:
        manager.root.show_error_popup('Unable to show git diff repo.', out)
    else:
        manager.diff_text_block.set_text(out)
        manager.diff_text_block.title = 'Git Diff'


def open_git_diff_file(manager):
    filename = manager.add_files_menu.get()[3:]
    out, err = pyautogit.commands.git_diff_file(filename)
    if err < 0:
        manager.root.show_error_popup('Unable to show git diff for file {}.'.format(filename), out)
    else:
        manager.diff_text_block.set_text(out)
        manager.diff_text_block.title = 'Git Diff - {}'.format(filename)


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