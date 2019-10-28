@echo off
REM ########################################################################
REM Argument %1: server identifier (matches a server in GUI XML)
REM Argument %2: context (spacecraft name)
REM ########################################################################

setlocal

REM ########################################################################
REM Setup of base directory
REM ########################################################################
call :dirname %0
call :dirname "%DIRNAME:~0,-1%"
set SPELL_HOME=%DIRNAME:~0,-1%\
call :dirname "%SPELL_HOME%"
set BASENAME=%DIRNAME:~0,-1%
set SERVER=%1
set SPACECRAFT=%2

REM ########################################################################
REM Main environment variables
REM ########################################################################
if "%SPELL_DATA%" == "" set SPELL_DATA=%SPELL_HOME%data
if "%SPELL_CONFIG%" == "" set SPELL_CONFIG=%BASENAME%\config
if "%SPELL_SYS_DATA%" == "" set SPELL_SYS_DATA=%SPELL_HOME%data
if "%SPELL_LOG%" == "" set SPELL_LOG=%DIRNAME%log

if not exist "%SPELL_LOG%" mkdir "%SPELL_LOG%"

echo Spacecraft  : %SPACECRAFT%
echo Server ID   : %SERVER%
echo SPELL home  : %SPELL_HOME%
echo SPELL data  : %SPELL_DATA%
echo SPELL config: %SPELL_CONFIG%

REM ########################################################################
REM Set GUI configuration Environment
REM ########################################################################

set __CTX__=%SPACECRAFT%
set __SRV__=%SERVER%

set LOGFILE="%SPELL_HOME%log\GUI-%SERVER%-%USERNAME%.log"
echo Log file is %LOGFILE%

REM ########################################################################
REM Launch the GUI
REM ########################################################################
cd %SPELL_HOME%
@echo on
start spel-gui.exe -Duser.timezone=UTC -clean -data @noDefault -config "%SPELL_CONFIG%\config.xml" -D__CTX__="%SPACECRAFT%" -D__SRV__="%SERVER%" -Dosgi.logfile=%LOGFILE%
@echo off

endlocal
goto :EOF

:dirname
set DIRNAME=%~dp1
goto :EOF
