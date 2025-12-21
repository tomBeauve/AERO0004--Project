echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent/ntbin/win64/winkill.exe"

start "tell.exe" /B "C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\tell.exe" laptop_tom 65091 CLEANUP_EXITING
timeout /t 1
"C:\PROGRA~1\ANSYSI~1\ANSYSS~1\v252\fluent\ntbin\win64\kill.exe" tell.exe
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 34548) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 30568) 
if /i "%LOCALHOST%"=="laptop_tom" (%KILL_CMD% 41876)
del "C:\Users\tbeau\Documents\Universite\MASTER1\Turbulent Flows\Project\AERO0004--Project\ConvergenceStudy\1Residuals\TOLe-7\cleanup-fluent-laptop_tom-30568.bat"
