# pyautogit [![PyPI version](https://badge.fury.io/py/pyautogit.svg)](https://badge.fury.io/py/pyautogit)

A command line interface for working with git written in python with the help of [py_cui](https://github.com/jwlodek/py_cui).

### Installation

An obvious prerequisit to installing `pyautogit` is to have `git` installed and in your system path. You will also require python 3.4+, and
`python3` and `python` must be reachable on your system `PATH` for operations that require git credentials.
Once this is done, you may install the module.

To install `pyautogit`, it is recommended to use `pip`:
```
pip install pyautogit
```
This will also install `py_cui`, the Command Line UI builder library upon which the project is based, and `windows-curses` if running on windows, which is a `curses` emulator for the win32 platform.

Alternatively, you can install from source. Clone this repository and use `pip` to install:
```
git clone https://github.com/jwlodek/pyautogit
cd pyautogit
pip install .
```
If `pyautogit` is already installed and you would like to update it, use:
```
pip install --upgrade pyautogit
```
or
```
cd pyautogit
git pull
pip install --upgrade .
```
if updating a local version.

Note that you may require root access for installing with `pip` depending on your system's python configuration.

### Demo

Below is a quick demo of using `pyautogit to do some common git actions.

### Usage

Once `pyautogit` is installed, open a command line client (note that Windows Terminal is not yet supported), then navigate to a directory and type:
```
pyautogit
```
You can also specify an external directory:
```
pyautogit -w /home/jwlodek/repos
```
If you open `pyautogit` in a directory that contains a `.git` folder, it will treat it as a repository, while if it cannot find said folder, the target location will be treated as a workspace.

Use the keyboard shortcut descriptions listed in the status bar at the bottom of the window to navigate the interface and menus.

### License

BSD 3-Clause License

Copyright (c) 2020, Jakub Wlodek
All rights reserved.