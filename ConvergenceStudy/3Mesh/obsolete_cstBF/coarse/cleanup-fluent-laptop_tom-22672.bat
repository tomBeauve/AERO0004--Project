echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\tell.exe" laptop_tom 56989 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 13120) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 22672) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 39280)
del "C:\Users\tbeau\Documents\Universite\MASTER1\Turbulent Flows\Project\AERO0004--Project\ConvergenceStudy\3Mesh\coarse\cleanup-fluent-laptop_tom-22672.bat"
