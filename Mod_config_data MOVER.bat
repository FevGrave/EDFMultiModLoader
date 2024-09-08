@echo off
setlocal

:: Set the target directory
set "targetDir=%CD%\Mods\EDF 6 MOD SETTINGS MAKER\MOD CONFIG DATA PLACED HERE"

:: Create the target directory if it doesn't exist
if not exist "%targetDir%" (
    mkdir "%targetDir%"
)

:: Move all *Mod_config_data.json files in the current directory to the target directory
for %%f in (*Mod_config_data.json) do (
    if exist "%%f" (
        move "%%f" "%targetDir%"
    )
)

:: End the script
exit /b %ERRORLEVEL%
