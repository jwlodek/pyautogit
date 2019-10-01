"""
This file contains all definitions and functions for git commands 
used by pyautogit. This file should remain separate from the CUI interface.

Author: Jakub Wlodek
Created: 01-Oct-2019
"""

import os
from sys import platform
from subprocess import Popen, PIPE

if platform == "win32":
    import wexpect as EXPECT
else:
    import pexpect as EXPECT


def git_enter_uname_password(credentials):
    uname = credentials[0]
    passwd = credentials[1]



def git_status(repo_path):
    err = 0
    message = None
    try:
        proc = Popen(['git', '-C', repo_path, 'status'], stdout=PIPE, stderr=PIPE)
        out, error = proc.communicate()
        message = out.decode()
    except:
        err = -1
        message = "Unknown error"

    return err, message



def git_init_new_repo(new_dir_target):
    err = 0
    message = None
    if os.path.exists(new_dir_target):
        err = -1
        message = "Path already exists"
    else:
        try:
            os.mkdir(new_dir_target)
            readme_fp = open(os.path.join(new_dir_target, 'README.md'), 'w')
            readme_fp.write('# {}'.format(new_dir_target))
            readme_fp.close()
            proc = Popen(['git', 'init', new_dir_target], stdout=PIPE, stderr=PIPE)
            out, error = proc.communicate()
            message = out.decode()
        except PermissionError:
            err = -1
            message = "Permission error when initializing git repo"
        except OSError:
            err = -1
            message = "Unable to create directory"
        except:
            err = -1
            message = "Unknown error"


    return err, message


def git_clone_new_repo(new_repo_url, credentials):
    err = 0
    message = None