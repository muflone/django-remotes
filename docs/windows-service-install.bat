CD /D %~dp0
NSSM install django-remotes-client "%CD%\client.exe" "--action commands_monitor --settings %CD%\client.ini --interval 10"
NSSM set django-remotes-client DisplayName "Django Remotes client"
NSSM set django-remotes-client Description "Monitor commands from Django Remotes server"
CALL "windows-service-start.bat"
