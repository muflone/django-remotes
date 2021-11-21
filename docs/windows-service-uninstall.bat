CD /D %~dp0
CALL "windows-service-stop.bat"
NSSM remove django-remotes-client confirm
