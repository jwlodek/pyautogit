"""
This file contains all definitions and functions for git commands 
used by pyautogit. This file should remain separate from the CUI interface.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import os
from os import environ
import re
import shutil
import stat
from sys import platform
from subprocess import Popen, PIPE
import pyautogit.askpass as ASKPASS


def remove_repo_tree(target):
    if os.path.exists(target) and os.path.isdir(target):
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)
        shutil.rmtree(target, onerror=del_rw)


def handle_credential_command(command, credentials, target_location='.'):
    out = ''
    err = 0
    # This is a bit janky, but I'm not sure what I could do to make it better
    askpass_dir = os.path.dirname(ASKPASS.__file__)
    if platform == "win32":
        askpass_script = "askpass_win.py"
    else:
        askpass_script = "askpass.py"
    askpass_script_path = os.path.join(askpass_dir, askpass_script)
    environ['GIT_ASKPASS'] = askpass_script_path
    environ['GIT_USERNAME'] = credentials[0]
    environ['GIT_PASSWORD'] = credentials[1]
    out, err = handle_basic_command(command, command)

    return out, err
        


def handle_basic_command(command, name, remove_quotes=True):
    out = None
    err = 0
    if '"' in command:
        run_command = []
        strings = re.findall('"[^"]*"', command)
        non_strings = re.split('"[^"]*"', command)
        for i in range(len(strings)):
            run_command = run_command + non_strings[i].strip().split(' ')
            string_in = strings[i]
            if remove_quotes:
                string_in = string_in[1:]
                string_in = string_in[:(len(string_in) - 1)]
            run_command.append(string_in)
        if len(non_strings) == (len(strings) + 1) and len(non_strings[len(strings)]) > 0:
            run_command.append(non_strings[len(strings) + 1])
    else:
        run_command = command.split(' ')
    try:
        proc = Popen(run_command, stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if proc.returncode != 0:
            out = error.decode()
            err = -1
        else:
            out = output.decode()
    except:
        out = "Unknown error processing function: {}".format(name)
        err = -1
    return out, err


def handle_open_external_program_command(command, name):
    out = None
    err = 0
    run_command = command.split(' ')
    try:
        proc = Popen(run_command, stdout=PIPE, stderr=PIPE)
        out = "Opened external program"
    except:
        out = "Unknown error processing function: {}".format(name)
        err = -1
    return out, err


def git_status_short(repo_path='.'):

    command = "git -C {} status -s".format(repo_path)
    name = "git_short_status"
    return handle_basic_command(command, name)


def git_status(repo_path='.'):

    command = "git -C {} status".format(repo_path)
    name = "git_short_status"
    return handle_basic_command(command, name)


def git_get_remotes():
    command = "git remote"
    name = "git_get_remotes"
    return handle_basic_command(command, name)

def git_get_remote_info(remote):
    command = 'git remote show -n {}'.format(remote)
    name='git_get_remote_info'
    return handle_basic_command(command, name)


def git_get_branches():
    command = "git branch"
    name = "git_get_branches"
    return handle_basic_command(command, name)


def git_get_recent_commits(branch):
    command = "git --no-pager log {} --oneline".format(branch)
    name = "git_get_recent_commits"
    return handle_basic_command(command, name)


def git_init_new_repo(new_dir_target):
    if os.path.exists(new_dir_target):
        err = -1
        out = "Path already exists"
    else:
        os.mkdir(new_dir_target)
        readme_fp = open(os.path.join(new_dir_target, 'README.md'), 'w')
        readme_fp.write('# {}'.format(new_dir_target))
        readme_fp.close()
        command = 'git init {}'.format(new_dir_target)
        name = 'git_init_new_repo'
        out, err = handle_basic_command(command, name)

    return out, err


def git_clone_new_repo(new_repo_url, credentials):
    out = None
    err = 0
    if os.path.exists(new_repo_url.split('/')[-1]):
        err = -1
        out = "The target repo couldn't be cloned - Directory exists"
    else:
        command = 'git clone {}'.format(new_repo_url)
        out, err = handle_credential_command(command, credentials)
        if err == 0:
            out = "Successfully cloned {}".format(new_repo_url)
            
    return out, err


def git_add_all():
    command = 'git add -A'
    name = 'git_add_all'
    return handle_basic_command(command, name)


def git_add_file(filename):
    command = 'git add {}'.format(filename)
    name = 'git_add_file'
    return handle_basic_command(command, name)


def git_reset_file(filename):
    command = 'git reset HEAD {}'.format(filename)
    name = 'git_reset_file'
    return handle_basic_command(command, name)

def git_create_new_branch(branchname, checkout=True):
    command = 'git checkout -b {}'.format(branchname)
    name = 'git_create_new_branch'
    return handle_basic_command(command, name)


def git_checkout_branch(branchname):
    command = 'git checkout {}'.format(branchname)
    name = 'git_checkout_branch'
    return handle_basic_command(command, name)


def git_stash_all():
    command = 'git stash'
    name = 'git_stash_all'
    return handle_basic_command(command, name)

def git_stash_file(filename):
    command = 'git stash {}'.format(filename)
    name = 'git_stash_file'
    return handle_basic_command(command, name)


def git_stash_pop():
    command = 'git stash pop'
    name = 'git_stash_pop'
    return handle_basic_command(command, name)


def git_log(branch):
    command = 'git --no-pager log {}'.format(branch)
    name='git_log'
    return handle_basic_command(command, name)


def git_diff():
    command = 'git diff'
    name='git_diff'
    return handle_basic_command(command, name)


def git_diff_file(filename):
    command = 'git diff {}'.format(filename)
    name='git_diff_file'
    return handle_basic_command(command, name)


def git_pull_branch(branch, remote, credentials):
    command = 'git pull {} {}'.format(remote, branch)
    return handle_credential_command(command, credentials)



def git_push_to_branch(branch, remote, credentials, repo_path='.'):
    out = None
    err = 0
    command = 'git push {} {}'.format(remote, branch)
    out, err = handle_credential_command(command, credentials)
    if err == 0:
        out = "Pushed to branch successfully"

    return out, err


def open_default_editor(default_editor, path):
    command = '{} {}'.format(default_editor, path)
    name = "open_default_editor"
    return handle_open_external_program_command(command, name)


def git_commit_changes(commit_message):
    if len(commit_message) == 0:
        return "No commit message entered", -1
    else:
        command = 'git commit -m "{}"'.format(commit_message)
        name = "git_commit_changes"
        return handle_basic_command(command, name)

def git_add_remote(remote_name, remote_url):
    command = 'git remote add {} {}'.format(remote_name, remote_url)
    name = 'git_add_remote'
    return handle_basic_command(command, name)