@echo OFF
if exist npdoc2md goto SCRIPTEXIST
git clone https://github.com/jwlodek/npdoc2md
:SCRIPTEXIST
cd npdoc2md
git pull
py npdoc2md.py -i ..\..\..\pyautogit -o ..\..\DocstringGenerated -s __main__.py askpass.py askpass_win.py errors.py