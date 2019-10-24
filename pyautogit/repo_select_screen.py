"""
File contains a screen for listing available repos in pyautogit workspace.
"""

import py_cui
import pyautogit
import pyautogit.commands


def delete_repo(manager):
    target = manager.repo_menu.get()
    pyautogit.commands.remove_repo_tree(target)
    manager.repo_menu.remove_selected_item()


def update_status(manager):
    status_message = 'Current workspace directory:\n{}\n\n'.format(manager.top_path)
    status_message = status_message + 'Current repos loaded in workspace: {}\n'.format(len(manager.repos))
    if len(manager.credentials) == 0:
        status_message = status_message + 'Git Remote Credentials Not Entered'
    else:
        status_messge = status_message + 'Git Remote Credentials Entered'
    manager.current_status_box.set_text(status_message)


def show_repo_status(manager):
    repo_name = manager.repo_menu.get()
    manager.git_status_box.clear()
    out, err = pyautogit.commands.git_status(repo_name)
    if err != 0:
        manager.root.show_error_popup('Unable to get git status!', message)
    manager.git_status_box.set_text(out)
    manager.refresh_repos()


def clone_new_repo_cred(manager):
    if not manager.were_credentials_entered():
        manager.ask_credentials(callback=lambda : clone_new_repo(manager))
    else:
        clone_new_repo(manager)


def clone_new_repo(manager):
    new_repo_url = manager.clone_new_box.get()
    out, err = pyautogit.commands.git_clone_new_repo(new_repo_url, manager.credentials)
    if err != 0:
        manager.root.show_error_popup('Unable to clone repository!', out)
    else:
        manager.root.show_message_popup('Cloned new repository', out)
    manager.refresh_repos()


def create_new_repo(manager):
    new_dir_target = manager.create_new_box.get()
    err, message = pyautogit.commands.git_init_new_repo(new_dir_target)
    manager.root.title='{}, {}'.format(err, message)
    if err != 0:
        manager.root.show_error_popup('Unable to create new repository!', message)
    else:
        manager.root.show_message_popup('Created new repository', message)
    manager.create_new_box.clear()
    manager.refresh_repos()




