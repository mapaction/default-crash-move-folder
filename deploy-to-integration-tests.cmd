:: Copy the files
robocopy %~dp0%2 ^
 %1 ^
 /mir ^
 /log:%~dp0deploy-to-integration-test.log ^
 /xd .git ^
 /xf .gitattributes ^
 /xf .gitignore ^
 /xf gocd.yaml ^
 /xf enable-empty-dir-in-github.txt ^
 /xd deploy-to-fileserver.cmd ^
 /xf deploy-to-fileserver.log ^
 /xf event_description.json ^
 /xd 2_Active_Data

robocopy %~dp0%2/GIS/2_Active_Data/200_data_name_lookup ^
 %1/GIS/2_Active_Data/200_data_name_lookup ^
 /mir ^
 /log+:%~dp0deploy-to-integration-test.log ^
 /xd .git ^
 /xf .gitattributes ^
 /xf .gitignore ^
 /xf enable-empty-dir-in-github.txt ^

:: Check the error code (anything less than 8 is OK.
:: Greater or equal to 8 is a fail)
if %errorlevel% lss 8 goto finish

exit /b %errorlevel%

:finish
exit /b 0
