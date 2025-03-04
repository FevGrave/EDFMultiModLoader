@echo off
setlocal enabledelayedexpansion

:: Prompt the user for the number of files to create
set /p count="Enter the number of files to create: "

:: Check if the input is a valid positive number
if not defined count (
    echo Please enter a valid number.
    exit /b 1
)

:: Loop to create files from 001 to the specified number
for /l %%i in (1,1,%count%) do (
    :: Format the number with leading zeros to have three digits
    set num=00%%i
    set num=!num:~-3!

    :: Create the file with the formatted name
    echo {} > !num!Mod_config_data.json
    echo Created !num!Mod_config_data.json
)

exit /b %ERRORLEVEL%
