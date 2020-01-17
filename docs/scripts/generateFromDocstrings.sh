#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "markdoc" ]
then
git clone https://github.com/jwlodek/markdoc
fi
cd markdoc
python3 markdoc.py ../../../pyautogit/__init__.py ../../DocstringGenerated/PyAutogitManager.md
python3 markdoc.py ../../../pyautogit/screen_manager.py ../../DocstringGenerated/ScreenManager.md
python3 markdoc.py ../../../pyautogit/commands.py ../../DocstringGenerated/Commands.md
python3 markdoc.py ../../../pyautogit/repo_select_screen.py ../../DocstringGenerated/RepoSelect.md
python3 markdoc.py ../../../pyautogit/repo_control_screen.py ../../DocstringGenerated/RepoControl.md
