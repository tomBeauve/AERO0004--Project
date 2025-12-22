echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\tell.exe" laptop_tom 50913 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 43048) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 32212) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 22176)
del "C:\Users\tbeau\Documents\Universite\MASTER1\Turbulent Flows\Project\AERO0004--Project\ConvergenceStudy\3Mesh\BIS\xxfineBis\cleanup-fluent-laptop_tom-32212.bat"
