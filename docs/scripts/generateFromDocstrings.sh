#!/bin/bash

#Simple bash script for generating markdown documentation from docstrings

if [ ! -d "npdoc2md" ]
then
git clone https://github.com/jwlodek/npdoc2md
fi
cd npdoc2md
git pull
python3 npdoc2md.py -i ../../../pyautogit -o ../../DocstringGenerated -s __main__.py askpass.py askpass_win.py errors.py

