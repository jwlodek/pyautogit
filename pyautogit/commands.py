"""
This file contains all definitions and functions for git commands 
used by pyautogit. This file should remain separate from the CUI interface.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import os
import shutil
from sys import platform
from subprocess import Popen, PIPE

if platform == "win32":
    import wexpect as EXPECT
else:
    import pexpect as EXPECT


def remove_repo_tree(target):
    if os.path.exists(target) and os.path.isdir(target):
        shutil.rmtree(target)


def handle_credential_command(command, credentials, target_location='.'):
    try:
        child = EXPECT.spawn(command)
        child.expect('Username*')
        child.sendline(credentials[0])
        child.expect('Password*')
        child.sendline(credentials[1])
        child.wait()
    
    # In the case that we weren't prompted for uname and pass, don't throw exception.
    except EXPECT.exceptions.EOF:
        pass


def handle_basic_command(command, name):
    out = None
    err = 0
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

def git_get_branches():
    command = "git branch"
    name = "git_get_branches"
    return handle_basic_command(command, name)


def git_get_recent_commits(branch):
    command = "git --no-pager log {} --oneline".format(branch)
    name = "git_get_recent_commits"
    return handle_basic_command(command, name)


def git_init_new_repo(new_dir_target):
    out = None
    err = 0
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
        handle_credential_command(command, credentials)
        out = "Successfully cloned {}".format(new_repo_url)
    return out, err


def git_add_all():
    command = 'git add -A'
    name = 'git_add_all'
    return handle_basic_command(command, name)


def git_add_file(filename):
    command = 'git add filename'
    name = 'git_add_file'
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


def git_diff(repo_path = '.'):
    command = 'git diff'
    name='git_diff'
    return handle_basic_command(command, name)


def git_pull_branch(branch, remote):
    command = 'git pull {} {}'.format(remote, branch)
    name = 'git_pull_branch'
    return handle_basic_command(command, name)


def git_push_to_branch(branch, remote, credentials, repo_path='.'):
    out = None
    err = 0
    if os.path.exists(new_repo_url.split('/')[-1]):
        err = -1
        message = "The target repo couldn't be cloned - Directory exists"
    else:
        try:
            command = 'git push {} {}'.format(remote, branch)
            handle_credential_command(command, credentials)
            out = "Pushed to branch successfully"
        except:
            err = -1
            out = "Failed to clone {}".format(new_repo_url)

    return out, err