# pyautogit Installation

An obvious prerequisit to installing `pyautogit` is to have `git` installed an in your system path. Once this is done, you may install the module.

To install `pyautogit`, it is recommended to use `pip`:
```
pip install pyautogit
```
This will also install `py_cui`, the Command Line UI builder library upon which the project is based, and `windows-curses` on windows systems, which is required for `py_cui` on windows machines.

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