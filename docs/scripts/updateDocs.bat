@echo OFF

cd ..\..\..
if exist pyatutogit-docs goto DOCSEXIST
git clone https://github.com/jwlodek/pyautogit-docs
:DOCSEXIST
cd pyautogit
git pull
py -m mkdocs build -d ..\pyautogit-docs
cd ..\pyautogit-docs
git add -A
git commit -m "Update pyautogit docs %date%"
git push