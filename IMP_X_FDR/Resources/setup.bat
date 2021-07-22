@echo off

"python\python.exe" -m pip uninstall numpy scipy -y
"python\python.exe" -m pip install -r requirements.txt

pause