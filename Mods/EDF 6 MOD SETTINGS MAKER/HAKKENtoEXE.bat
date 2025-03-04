@echo off
cd /d "%~dp0"
pyinstaller --noconfirm --name "EDF HAKKEN" --noconsole ^
--add-data "ConfigBuilder.py;." ^
--add-data "GamemodeConfig.py;." ^
--add-data "ConfigWeaponCuller.py;." ^
--add-data "ConfigWeaponAppender.py;." ^
--add-data "ConfigCompressor.py;." ^
--add-data "ConfigStringReplacer9000.py;." ^
--add-data "ConfigSubtitleAppender.py;." ^
--add-data "ConfigTextBuilder.py;." ^
--add-data "ConfigWeaponAppender.py;." ^
--add-data "ImportDefaultData.json;." ^
--add-data "ImportSubtitleVoiceTable.CN.json;." ^
--add-data "ImportSubtitleVoiceTable.EN.json;." ^
--add-data "ImportSubtitleVoiceTable.JA.json;." ^
--add-data "ImportSubtitleVoiceTable.KR.json;." ^
--add-data "ImportSubtitleVoiceTable.SC.json;." ^
--add-data "ImportTextTable-CN.json;." ^
--add-data "ImportTextTable-EN.json;." ^
--add-data "ImportTextTable-JA.json;." ^
--add-data "ImportTextTable-KR.json;." ^
--add-data "ImportTextTable-SC.json;." ^
--add-data "ImportWeaponTable.json;." ^
--add-data "ImportWeaponTextTable-CN.json;." ^
--add-data "ImportWeaponTextTable-EN.json;." ^
--add-data "ImportWeaponTextTable-JA.json;." ^
--add-data "ImportWeaponTextTable-KR.json;." ^
--add-data "ImportWeaponTextTable-SC.json;." ^
--hidden-import "os" ^
--hidden-import "json" ^
--version-file "hakken_version_info.txt" ^
--onefile ^
"%cd%\ConfigBuildAll.py"

set "dist_folder=%CD%\dist"
set "exe_file=%dist_folder%\EDF HAKKEN.exe"
set "destination=%CD%\.."
set "destinationpushsc=%CD%\..\..\EDFModloaderHead\Mods\EDF 6 MOD SETTINGS MAKER"

REM Check if the build was successful
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build for EDF HAKKEN failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

REM Ensure the target folder exists and copy the executable
IF EXIST "%exe_file%" (
    if not exist "%mod_folder%" (
        mkdir "%mod_folder%"
    )
    copy "%exe_file%" "%CD%"
    copy "%exe_file%" "%destinationpushsc%"

    IF %ERRORLEVEL% EQU 0 (
        echo EDF HAKKEN copied to "CD" successfully!
    ) ELSE (
        echo Failed to copy EDF HAKKEN. Exiting...
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo EDF HAKKEN executable not found. Exiting...
    pause
    exit /b 1
)