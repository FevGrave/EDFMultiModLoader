@echo off
cd /d "%~dp0"
REM Part 0: Build and move WeaponStarResultFormula executable

pyinstaller --noconfirm --name "WSLRF" --noconsole ^
--version-file "wslrf_version_info.txt" ^
--onefile ^
"%CD%\WSLRF.py"

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build for WSRLF failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

set "dist_folder=%CD%\dist"
set "exe_file=%dist_folder%\WSLRF.exe"
set "destination=%CD%\.."
set "destinationpush=%CD%\..\EDFModloaderHead"
set "destinationpushsc=%CD%\..\EDFModloaderHead\EDFModloaderHead_B"

IF EXIST "%exe_file%" (
    copy "%exe_file%" "%CD%"
    copy "%exe_file%" "%destination%"
    copy "%exe_file%" "%destinationpush%"
    copy "%exe_file%" "%destinationpushsc%"
    IF %ERRORLEVEL% EQU 0 (
        echo ProgressTrackerPercent copied successfully!
    ) ELSE (
        echo Failed to copy WSLRF executable. Exiting...
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo WSLRF executable not found. Exiting...
    pause
    exit /b 1
)

REM Part 1: Build and move WeaponStatCreator executable

pyinstaller --noconfirm --name "WeaponStatCreator" --noconsole ^
--version-file "wsc_version_info.txt" ^
--onefile ^
"%CD%\WeaponStatCreator.py"

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build for WeaponStatCreator failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

set "dist_folder=%CD%\dist"
set "exe_file=%dist_folder%\WeaponStatCreator.exe"
set "destination=%CD%\.."
set "destinationpush=%CD%\..\EDFModloaderHead"
set "destinationpushsc=%CD%\..\EDFModloaderHead\EDFModloaderHead_B"

IF EXIST "%exe_file%" (
    copy "%exe_file%" "%CD%"
    copy "%exe_file%" "%destination%"
    copy "%exe_file%" "%destinationpush%"
    copy "%exe_file%" "%destinationpushsc%"
    IF %ERRORLEVEL% EQU 0 (
        echo ProgressTrackerPercent copied successfully!
    ) ELSE (
        echo Failed to copy WeaponStatCreator executable. Exiting...
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo ProgressTrackerPercent executable not found. Exiting...
    pause
    exit /b 1
)


REM Part 2: Build and move ProgressTrackerPercent executable

pyinstaller --noconfirm --name "ProgressTrackerPercent" --noconsole ^
--hidden-import "os" ^
--version-file "ptp_version_info.txt" ^
--onefile ^
"%CD%\ProgressTrackerPercent.py"

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build for ProgressTrackerPercent failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

set "dist_folder=%CD%\dist"
set "exe_file=%dist_folder%\ProgressTrackerPercent.exe"
set "destination=%CD%\.."
set "destinationpush=%CD%\..\EDFModloaderHead"
set "destinationpushsc=%CD%\..\EDFModloaderHead\EDFModloaderHead_B"

IF EXIST "%exe_file%" (
    copy "%exe_file%" "%CD%"
    copy "%exe_file%" "%destination%"
    copy "%exe_file%" "%destinationpush%"
    copy "%exe_file%" "%destinationpushsc%"
    IF %ERRORLEVEL% EQU 0 (
        echo ProgressTrackerPercent copied successfully!
    ) ELSE (
        echo Failed to copy ProgressTrackerPercent executable. Exiting...
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo ProgressTrackerPercent executable not found. Exiting...
    pause
    exit /b 1
)

REM Part 3: Build and move EDF MML executable # 

pyinstaller --noconfirm --name "EDF MML" --clean --noconsole ^
--add-data "fonts/RobotoCondensed-Bold.TTF;fonts" ^
--add-data "EDF_ModloaderHeadFunc.py;." ^
--add-data "ConfigManifestUninstaller.py;." ^
--add-data "ProgressTrackerPercent.exe;." ^
--add-data "ImageResources.py;." ^
--add-data "images/*;images" ^
--add-data "languages/*;languages" ^
--add-data "Icon_256.ico;." ^
--add-data "eggs.py;." ^
--hidden-import "PIL" ^
--hidden-import "requests" ^
--hidden-import "tkinter.filedialog" ^
--hidden-import "shutil" ^
--hidden-import "watchdog" ^
--hidden-import "os" ^
--version-file "version_info.txt" ^
--onefile ^
--icon "Icon_256.ico" ^
"%CD%\EarthDefenseForceModloaderHead.py"

IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build for EDF MML failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

set "exe_file2=%dist_folder%\EDF MML.exe"

IF EXIST "%exe_file2%" (
    copy "%exe_file2%" "%destination%"
    copy "%exe_file2%" "%destinationpush%"
    IF %ERRORLEVEL% EQU 0 (
        echo EDF MML copied successfully!
    ) ELSE (
        echo Failed to copy EDF MML executable. Exiting...
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo EDF MML executable not found. Exiting...
    pause
    exit /b 1
)

echo All builds and copies completed successfully!
exit /b %ERRORLEVEL%
