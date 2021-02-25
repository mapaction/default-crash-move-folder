:: Copy the files
robocopy %~dp0 ^
 ./default-crash-move-folder ^
 /mir ^
 /log:%~dp0deploy-to-fileserver.log ^
 /xd .git ^
 /xf .gitattributes ^
 /xf .gitignore ^
 /xf gocd.yaml ^
 /xf enable-empty-dir-in-github.txt ^
 /xd deploy-to-fileserver.cmd ^
 /xf deploy-to-fileserver.log

:: Check the error code (anything less than 8 is OK.
:: Greater or equal to 8 is a fail)
if %errorlevel% lss 8 goto finish

exit /b %errorlevel%

:finish
exit /b 0
