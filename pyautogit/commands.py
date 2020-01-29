"""File containing all definitions and functions for git commands used by pyautogit.

This file should remain separate from the CUI interface.

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
import pyautogit.logger as LOGGER


def remove_repo_tree(target):
    """Function that removes repository.

    Required since removing git repos on windows require a chmod operation.

    Parameters
    ----------
    target : str
        Dir path to removed repo
    """

    if os.path.exists(target) and os.path.isdir(target):
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)
        shutil.rmtree(target, onerror=del_rw)


def handle_credential_command(command, credentials, target_location='.'):
    """Function that executes a git command that requires credentials.

    Parameters
    ----------
    command : str
        String command to run
    credentials : list of str
        The user's entered git remote credentials
    target_location : str
        Location of repository
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

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
    """Function that executes any git command given, and returns program output.

    Parameters
    ----------
    command : str
        The command string to run
    name : str
        The name of the command being run
    remove_quotes : bool
        Since subprocess takes an array of strings, we split on spaces, however in some cases we want quotes to remain together (ex. commit message)
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

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
            err = proc.returncode
        else:
            out = output.decode()
    except:
        out = "Unknown error processing function: {}".format(name)
        err = -1
    return out, err


def handle_open_external_program_command(command, name):
    """Function used to run commands that open an external program and detatch from pyautogit.

    Parameters
    ----------
    command : str
        Command string to run
    name : str
        Name of command to run
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    run_command = command.split(' ')
    try:
        proc = Popen(run_command, stdout=PIPE, stderr=PIPE)
        out, err_messg = proc.communicate()
        err = proc.returncode
        if err != 0:
            out = err_messg.decode()
        else:
            out = out.decode()
    except FileNotFoundError:
        out = "Program: {} could not be found in system path".format(command.split(' ')[0])
        err = -1
    except:
        out = "Unknown error processing function: {}".format(name)
        err = -1
    return out, err


def handle_custom_command(command):
    """Function that executes a custom, non-git command

    Patameters
    ----------
    command : str
        Command string to run

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    name = command
    return handle_basic_command(command, name)


def open_default_editor(default_editor, path):
    """Function used to open the selected default editor in external window.

    Parameters
    ----------
    default_editor : str
        Editor open command. ex: emacs, code
    path : str
        The path to the file or directory to open

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = '{} {}'.format(default_editor, path)
    name = "open_default_editor"
    return handle_open_external_program_command(command, name)


#####################################################################
#                                                                   #
#                   Git Command Functions Below                     #
#                                                                   #
#####################################################################

#---------------------#
# Git Status Commands #
#---------------------#

def git_status_short(repo_path='.'):
    """Function for getting shorthand git status

    Parameters
    ----------
    repo_path : str
        Target repo path

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = "git -C {} status -s".format(repo_path)
    name = "git_short_status"
    return handle_basic_command(command, name)


def git_status(repo_path='.'):
    """Function for getting git status

    Parameters
    ----------
    repo_path : str
        Target repo path

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = "git -C {} status".format(repo_path)
    name = "git_short_status"
    return handle_basic_command(command, name)


def git_tree(branch):
    """Function that gets git log as a tree

    Parameters
    ----------
    branch : str
        branch or tag name to log

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git --no-pager log --oneline --decorate --all --graph {}'.format(branch)
    name = 'git_tree'
    return handle_basic_command(command, name)


def git_log(branch):
    """Function that gets git log information

    Parameters
    ----------
    branch : str
        branch or tag name to log

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git --no-pager log {}'.format(branch)
    name='git_log'
    return handle_basic_command(command, name)


def git_diff():
    """Function that gets git diff

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git diff'
    name='git_diff'
    return handle_basic_command(command, name)


def git_diff_file(filename):
    """Function that gets git diff for specific file

    Parameters
    ----------
    filename : str
        Name of file to diff

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git diff {}'.format(filename)
    name='git_diff_file'
    return handle_basic_command(command, name)


#---------------------#
# Git Remote Commands #
#---------------------#

def git_get_remotes():
    """Function for returning git remotes list

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = "git remote"
    name = "git_get_remotes"
    return handle_basic_command(command, name)


def git_get_remote_info(remote):
    """Function that gets information about a remote

    Parameters
    ----------
    remote : str
        Name of target remote

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git remote show -n {}'.format(remote)
    name='git_get_remote_info'
    return handle_basic_command(command, name)


def git_add_remote(remote_name, remote_url):
    """Function that adds a new remote to the repository

    Parameters
    ----------
    remote_name : str
        Name of the new remote
    remote_url : str
        URL of the new remote

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git remote add {} {}'.format(remote_name, remote_url)
    name = 'git_add_remote'
    return handle_basic_command(command, name)


def git_remove_remote(remote_name):
    """Function that removes a remote from the repository

    Parameters
    ----------
    remote_name : str
        Name of the remote

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git remote rm {}'.format(remote_name)
    name = 'git_remove_remote'
    return handle_basic_command(command, name)


def git_rename_remote(remote, new_name):
    """Function that renames a remote in the repository

    Parameters
    ----------
    remote : str
        Old name of the remote
    new_name : str
        New name of the new remote

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git remote rename {} {}'.format(remote, new_name)
    name = 'git_rename_remote'
    return handle_basic_command(command, name)


#---------------------#
# Git Commit Commands #
#---------------------#

def git_get_commit_info(commit_hash):
    """Function that gets info about a particular commit.

    Parameters
    ----------
    commit_hash : str
        Hash code for target commit

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git show {}'.format(commit_hash)
    name = 'git_get_commit_info'
    return handle_basic_command(command, name)


def git_checkout_commit(commit_hash):
    """Function that checks out a particular commit.

    Parameters
    ----------
    commit_hash : str
        Hash code for target commit

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git checkout {}'.format(commit_hash)
    name = 'git_checkout_commit'
    return handle_basic_command(command, name)


def git_commit_changes(commit_message):
    """Function that commits added changes

    Parameters
    ----------
    commit_message : str
        Message attached to target commit

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    if len(commit_message) == 0:
        return "No commit message entered", -1
    else:
        command = 'git commit -m "{}"'.format(commit_message)
        name = "git_commit_changes"
        return handle_basic_command(command, name)


def git_create_tag(tag_name):
    """Function that creates a new tag

    Parameters
    ----------
    tag_name : str
        The name of the new tag
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git tag {}'.format(tag_name)
    name = 'git_create_tag'
    return handle_basic_command(command, name)


def git_get_tags():
    """Function that gets list of git tags in repo
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git tag'
    name = 'git_get_tags'
    return handle_basic_command(command, name)

#---------------------#
# Git Branch Commands #
#---------------------#

def git_get_branches():
    """Function that gets a list of the repo branches.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = "git branch"
    name = "git_get_branches"
    return handle_basic_command(command, name)


def git_get_recent_commits(branch):
    """Gets recent commits made to the branch

    Parameters
    ----------
    branch : str
        Name of current branch

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git --no-pager log {} --oneline'.format(branch)
    name = "git_get_recent_commits"
    return handle_basic_command(command, name)


def git_create_new_branch(branch, checkout=True):
    """Creates anew branch for the repo

    Parameters
    ----------
    branch : str
        Name of new branch
    checkout : bool
        If true, checkout branch after creation.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git checkout -b {}'.format(branch)
    name = 'git_create_new_branch'
    return handle_basic_command(command, name)


def git_checkout_branch(branch):
    """Checks out given branch

    Parameters
    ----------
    branch : str
        Name of target branch

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git checkout {}'.format(branch)
    name = 'git_checkout_branch'
    return handle_basic_command(command, name)


def git_checkout_tag(tag):
    """Checks out given tag

    Parameters
    ----------
    tag : str
        Name of tag to check out
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git checkout -q {}'.format(tag)
    name = 'git_checkout_tag'
    return handle_basic_command(command, name)


def git_merge_branches(merge_branch):
    """Merges checked out branch with given branch

    Parameters
    ----------
    merge_branch : str
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git merge {}'.format(merge_branch)
    name = 'git_merge_branches'
    return handle_basic_command(command, name)


def git_revert_branch_merge():
    """Undos merge between two branches
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git reset --hard ORIG_HEAD'
    name = 'git_revert_branch_merge'
    return handle_basic_command(command, name)

#--------- ---------#
# Git Repo Commands #
#-------------------#

def git_init_new_repo(new_dir_target):
    """Function that creates a new git repository

    Parameters
    ----------
    new_dir_target : str
        Name of new repo
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

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
    """Function that clones a new git repository

    Parameters
    ----------
    new_repo_url : str
        URL of new repo
    credentials : list of str
        Username and Password for git remote
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

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

#------------------------#
# Git (Un)Stage Commands #
#------------------------#

def git_add_all():
    """Function that stages all files in repo for commit.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git add -A'
    name = 'git_add_all'
    return handle_basic_command(command, name)


def git_reset_all():
    """Function that unstages all files in repo for commit.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git reset HEAD'
    name = 'git_reset_all'
    return handle_basic_command(command, name)


def git_add_file(filename):
    """Function that stages single file in repo for commit.

    Parameters
    ----------
    filename : str
        Name of file to stage

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git add {}'.format(filename)
    name = 'git_add_file'
    return handle_basic_command(command, name)


def git_reset_file(filename):
    """Function that unstages single file in repo for commit.

    Parameters
    ----------
    filename : str
        Name of file to unstage

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git reset HEAD {}'.format(filename)
    name = 'git_reset_file'
    return handle_basic_command(command, name)


#--------------------#
# Git Stash Commands #
#--------------------#


def git_stash_all():
    """Function that stashes all changes in repo.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git stash'
    name = 'git_stash_all'
    return handle_basic_command(command, name)

def git_unstash_all():
    """Function that unstashes all changes in repo.

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """
    command = 'git stash pop'
    name = 'git_unstash_all'
    return handle_basic_command(command, name)


def git_stash_file(filename):
    """Function that stashes single file in repo.

    Parameters
    ----------
    filename : str
        Name of file to stash

    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git stash {}'.format(filename)
    name = 'git_stash_file'
    return handle_basic_command(command, name)


#------------------------#
# Git Push/Pull Commands #
#------------------------#

def git_pull_branch(branch, remote, credentials):
    """Function that pulls a branch from the remote repo
    
    Parameters
    ----------
    branch : str
        Name of current branch
    remote : str
        Name of remote
    credentials : list of str
        Username and Password of user for remoe
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git pull {} {}'.format(remote, branch)
    return handle_credential_command(command, credentials)


def git_push_to_branch(branch, remote, credentials, repo_path='.'):
    """Function that pushes a branch to the remote repo
    
    Parameters
    ----------
    branch : str
        Name of current branch
    remote : str
        Name of remote
    credentials : list of str
        Username and Password of user for remote
    repo_path : str
        The repository path
    
    Returns
    -------
    out : str
        Output string from stdout if success, stderr if failure
    err : int
        Error code if failure, 0 otherwise.
    """

    command = 'git push {} {}'.format(remote, branch)
    return handle_credential_command(command, credentials)
