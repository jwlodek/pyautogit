import pytest
import pyautogit.commands as COMMANDS
import tests.helper_test_funcs as HELPER



def test_git_add():
    target = ['git', 'add', '-A']
    actual = COMMANDS.parse_string_into_executable_command('git add -A', False)
    assert HELPER.compare_lists(target, actual)


def test_git_commit():
    target = ['git', 'commit', '-m', '"Hello World"']
    actual = COMMANDS.parse_string_into_executable_command('git commit -m "Hello World"', False)
    assert HELPER.compare_lists(target, actual)


def test_git_commit_rem_quotes():
    target = ['git', 'commit', '-m', 'Hello World']
    actual = COMMANDS.parse_string_into_executable_command('git commit -m "Hello World"', True)
    assert HELPER.compare_lists(target, actual)