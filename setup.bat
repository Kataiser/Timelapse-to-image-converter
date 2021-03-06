@echo off
chcp 65001
echo.
pushd %~dp0

pip install Pillow

::Attempts to start py launcher without relying on PATH
%SYSTEMROOT%\py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO attempt
%SYSTEMROOT%\py.exe -3 "install_ffmpeg.py"
PAUSE
GOTO end

::Attempts to start py launcher by relying on PATH
:attempt
py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO lastattempt
py.exe -3 "install_ffmpeg.py"
PAUSE
GOTO end

::As a last resort, attempts to start whatever Python there is
:lastattempt
python.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO message
python.exe "install_ffmpeg.py"
PAUSE
GOTO end

:message
echo Couldn't find a valid Python ^>3.6 installation. Python needs to be installed and available in the PATH environment
echo variable.
echo https://github.com/Kataiser/Timelapse-to-image-converter
PAUSE

:end
