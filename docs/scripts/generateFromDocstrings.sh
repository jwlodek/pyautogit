#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "npdoc2md" ]
then
git clone https://github.com/jwlodek/npdoc2md
fi
git pull
cd npdoc2md
python3 npdoc2md.py ../../../pyautogit ../../DocstringGenerated -i __main__.py askpass.py askpass_win.py

