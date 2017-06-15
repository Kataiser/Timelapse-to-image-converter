@echo off

set /p id="Enter video filename: "

%~dp0\ffmpeg.exe -i "%~dp0\%id%" -vf fps=30 "%~dp0\output\%%06d.png"

pause
exit