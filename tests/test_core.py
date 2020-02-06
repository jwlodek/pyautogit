import pytest

import os
import py_cui
import pyautogit

# Initialize our testing environment but don't start CUI
# Need to figure out how to make the below not crash. (Bug in py_cui)
#root = py_cui.PyCUI(5, 4)
#manager = pyautogit.PyAutogitManager(root, '.', 'repo', False, [])


def test_find_repos_in_path():
    repos = pyautogit.find_repos_in_path('..')
    assert 'pyautogit' in repos


def test_is_git_repo():
    assert pyautogit.is_git_repo('.')
    assert not pyautogit.is_git_repo('docs')


# The below tests do not run correctly because of a bug in py_cui
"""

def test_open_editor_window():
    assert manager.current_state == 'repo'
    manager.open_editor_window()
    assert manager.current_state == 'editor'
    assert manager.root.get_widget_set().widgets == manager.editor_widget_set.widgets
    manager.open_autogit_window()
    assert manager.current_state == 'repo'

def test_open_repo_select_window():
    test_path = os.path.dirname(os.getcwd())
    assert manager.current_state == 'repo'
    manager.open_editor_window()
    assert manager.current_state == 'workspace'
    assert os.getcwd() == test_path
    assert manager.root.get_widget_set().widgets == manager.repo_select_widget_set.widgets
    manager.open_autogit_window()
    assert manager.current_state == 'repo'


def test_open_settings_window():
    assert manager.current_state == 'repo'
    manager.open_editor_window()
    assert manager.current_state == 'settings'
    assert manager.root.get_widget_set().widgets == manager.settings_widget_set.widgets
    manager.open_autogit_window()
    assert manager.current_state == 'repo'

def test_open_autogit_window():
    assert manager.current_state == 'repo'
    manager.test_open_repo_select_window()
    assert manager.current_state == 'workspace'
    manager.test_open_autogit_window()
    assert manager.current_state == 'repo'
    assert manager.root.get_widget_set().widgets == manager.repo_control_widget_set.widgets

"""