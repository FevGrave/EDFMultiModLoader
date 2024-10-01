@echo off
:: Set the URL for the Python 3.10.1 installer
set "url=https://www.python.org/ftp/python/3.10.1/python-3.10.1-amd64.exe"
set "output=python-3.10.1-amd64.exe"

:: Set the internal switch to decide if the additional packages should be installed
:: Set USE_INTERNAL_BUILD=1 to enable internal build installations, 0 to disable
set USE_INTERNAL_BUILD=0

:: Prompt the user to specify the installation directory
set /p installDir="Enter the directory where you want to install Python (e.g., C:\Python310): "

:: Check if the specified directory exists; if not, create it
if not exist "%installDir%" (
    echo Directory does not exist. Creating "%installDir%"...
    mkdir "%installDir%"
    if %ERRORLEVEL% neq 0 (
        echo Failed to create the directory. Please check permissions and try again.
        exit /b %ERRORLEVEL%
    )
)

:: Step 1: Download the Python installer using curl
echo Downloading Python 3.10.1 installer...
curl -o "%output%" "%url%"
if %ERRORLEVEL% neq 0 (
    echo Failed to download the installer. Please check your internet connection or URL.
    exit /b %ERRORLEVEL%
)
echo Download completed successfully.

:: Step 2: Install Python silently to the specified directory and add it to PATH
echo Installing Python 3.10.1 to "%installDir%"...
"%output%" /quiet InstallAllUsers=1 TargetDir="%installDir%" PrependPath=1
if %ERRORLEVEL% neq 0 (
    echo Installation failed. Please try installing manually.
    exit /b %ERRORLEVEL%
)
echo Python 3.10.1 installed successfully to "%installDir%" and added to PATH.

:: Step 3: Optional internal build installations
if "%USE_INTERNAL_BUILD%" equ "1" (
    echo Internal build enabled. Installing additional dependencies...

    :: Upgrade pip
    echo Upgrading pip...
    "%installDir%\python.exe" -m pip install --upgrade pip --user
    if %ERRORLEVEL% neq 0 (
        echo Failed to upgrade pip. Ensure Python is installed and added to PATH.
        exit /b %ERRORLEVEL%
    )

    :: Install Pillow
    echo Installing Pillow...
    "%installDir%\Scripts\pip.exe" install Pillow
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Pillow. Please check your pip installation.
        exit /b %ERRORLEVEL%
    )

    :: Install requests
    echo Installing requests...
    "%installDir%\Scripts\pip.exe" install requests
    if %ERRORLEVEL% neq 0 (
        echo Failed to install requests. Please check your pip installation.
        exit /b %ERRORLEVEL%
    )

    echo Internal build installations completed.
) else (
    echo Skipping internal build installations.
)

echo All installations completed successfully.
echo Testing python window
python testpython.py
pause
exit /b 0
