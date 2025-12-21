echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\tell.exe" laptop_tom 57528 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 1684) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 27836) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 18132)
del "C:\Users\tbeau\OneDrive\Documents\Universite\MASTER1\Turbulent Flows\Project\AERO0004--Project\V1\cleanup-fluent-laptop_tom-27836.bat"
