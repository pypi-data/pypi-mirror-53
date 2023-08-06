@echo off
::GNOME Acquirer global starter script by Samer Afach
::Authored on 28.01.2017

::Working dir and drive when this batch was started
set "StartDir=%CD%"
set "StartDrive=%CD:~0,2%"

::The directory and drive and full path of the script
set "ScriptsDir=%~dp0"
set "ScriptDrive=%~d0"
set "ScriptPath=%~f0"
echo Switching drive to %ScriptDrive%
echo Switching directory to %ScriptsDir%
%ScriptDrive%

::Starting directory in the script drive
set "StartDir_ScriptDrive=%CD%"
set "StartDrive_ScriptDrive=%CD:~0,2%"

cd %ScriptsDir%
echo Calling GNOME Acquirer through Python
python gnomeacquirer.py
echo Rolling back to starting directory
cd %StartDir_ScriptDrive%
%StartDrive%
cd %StartDir%
