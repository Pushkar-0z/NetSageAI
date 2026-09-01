@echo off
set "PATH=C:\Users\MD FAIYAZ KHAN\AppData\Local\Programs\MinGit\cmd;%PATH%"
echo =======================================================
echo Pushing NetSage AI code to GitHub (main branch)...
echo =======================================================
echo.
git push -u origin main
echo.
if errorlevel 1 (
    echo [ERROR] Push failed. Check credentials above.
) else (
    echo [SUCCESS] Code successfully pushed to GitHub!
)
pause
