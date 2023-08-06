@echo off
rem Start edit using the appropriate Python interpreter
set CURRDIR=%~dp0
openfiles "edit" "%CURRDIR%..\..\pythonw.exe" "%CURRDIR%edit.pyw" %1 %2 %3 %4 %5 %6 %7 %8 %9
