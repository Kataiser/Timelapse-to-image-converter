@echo off

del /q "%~dp0\compressed\*.*"
del /q "%~dp0\output\*.*"

echo.
echo Cleanup done

pause
exit