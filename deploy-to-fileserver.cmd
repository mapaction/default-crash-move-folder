:: Copy the files
robocopy 
	%~dp0 ^
	\\192.168.106.24\SYSAdmin\testing\github-mirror\default-cmf ^
	/mir
	/log:deploy-to-fileserver.log
	/xd .git ^
	/xf .gitattributes ^
    /xf .gitignore ^
	/xf ftp.mapaction.org.crt ^
	/xf gocd.yaml ^

:: Check the error code (anything less than 8 is OK.
:: Greater or equal to 8 is a fail)
if %errorlevel% lss 8 goto finish

echo Something failed 
exit /b 8

:finish
exit /b 0