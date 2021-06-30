@echo off

"python\python.exe" -m pip uninstall numpy scipy matplotlib_venn venn -y
"python\python.exe" -m pip install numpy scipy matplotlib_venn venn

pause