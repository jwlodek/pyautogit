#!/bin/bash

cd ../../..
if [ ! -d "pyautogit-docs" ]
then
git clone https://github.com/jwlodek/pyautogit-docs
fi
cd pyautogit
pip3 install mkdocs
python3 -m mkdocs build -d ../pyautogit-docs
cd ../pyautogit-docs
git add -A
DATE=$(date)
git commit -m "Update pyautogit docs $DATE"
git push
