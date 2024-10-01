@echo off
REM Build the executable using PyInstaller with the .spec file and additional options
pyinstaller --noconfirm --name "EDF MML" --noconsole ^
--add-data "fonts/ARUDJINGXIHEIG30_BD.TTF;fonts" ^
--add-data "EDF_ModloaderHeadFunc.py;." ^
--add-data "ConfigManifestUninstaller.py;." ^
--add-data "ImageResources.py;." ^
--add-data "images/*;images" ^
--add-data "Icon_256.ico;." ^
--icon "Icon_256.ico" ^
--hidden-import "PIL" ^
--hidden-import "PIL._imaging" ^
--hidden-import "requests" ^
--hidden-import "threading" ^
--hidden-import "tkinter.filedialog" ^
--hidden-import "tkinter.messagebox" ^
--hidden-import "shutil" ^
--hidden-import "os" ^
--hidden-import "sys" ^
--version-file "version_info.txt" ^
"%CD%\EarthDefenseForceModloaderHead.py"
:: 


REM Check if the build was successful
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller build failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

::  REM Sign the executable using signtool
::  signtool sign /f "path_to_your_certificate.pfx" /p "your_certificate_password" /tr http://timestamp.digicert.com /td sha256 /fd ::  sha256 "dist\EDF MML.exe"
::  
::  REM Check if signing was successful
::  IF %ERRORLEVEL% NEQ 0 (
::      echo Signing failed. Exiting...
::      pause
::      exit /b %ERRORLEVEL%
::  )
::  
::  echo Build and signing completed successfully!
echo Build completed successfully!

