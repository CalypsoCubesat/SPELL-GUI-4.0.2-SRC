@echo off

set SPELL_GUI_WS=E:\workspace\%USERNAME%\SPELL_GUI_WS
set ECLIPSE_BASE=R:\NewSpellDev\build\eclipse-SDK-4.8M5-win32
set BUILD_BASE_DIR=%~DP0..\SPELL-GUI_build_win32
set JAVA=D:\Programs\Java\jdk1.8.0_25\bin\java
set SPELL_GUI_COTS=R:\NewSpellDev\build\eclipse-SDK-4.8M5-win32
set ORBIT_COTS_REPO=R:\NewSpellDev\build-repo
set PRODUCT=SPELL-GUI_headless.product
set JRE=absolute:R:\NewSpellGUI\jre-8u151-windows-i586\jre1.8.0_151\

set SPELL_GUI_REPO=%~DP0
set SPELL_GUI_REPO=%SPELL_GUI_REPO:~0,-1%

FOR /f %%i in ('dir /b %ECLIPSE_BASE%\eclipse\plugins\org.eclipse.equinox.launcher_*.jar') DO SET EQUINOX_LAUNCHER=%%i
FOR /f %%i in ('dir /b %ECLIPSE_BASE%\eclipse\plugins\org.eclipse.pde.build_*') DO SET PDE_PLUGIN=%%i

IF EXIST "%BUILD_BASE_DIR%" RMDIR /S /Q "%BUILD_BASE_DIR%" && timeout /T 3  > nul

mkdir %BUILD_BASE_DIR%
mkdir %BUILD_BASE_DIR%\plugins
mkdir %BUILD_BASE_DIR%\transformedRepos

echo Copying SPELL GUI files to build directory %BUILD_BASE_DIR%

copy "%SPELL_GUI_REPO%\win32_build.properties" "%BUILD_BASE_DIR%\build.properties"

xcopy /s /c /q "%SPELL_GUI_REPO%" "%BUILD_BASE_DIR%\plugins"

IF NOT EXIST "%BUILD_BASE_DIR%\eclipse.build" mkdir %BUILD_BASE_DIR%\eclipse.build && mkdir %BUILD_BASE_DIR%\eclipse.build\features
copy %BUILD_BASE_DIR%\plugins\com.astra.ses.spell.gui\%PRODUCT% %BUILD_BASE_DIR%\eclipse.build\features\SPELL-GUI.product

@echo on
%JAVA% -jar %ECLIPSE_BASE%\eclipse\plugins\%EQUINOX_LAUNCHER% -application org.eclipse.ant.core.antRunner -buildfile %ECLIPSE_BASE%\eclipse\plugins\%PDE_PLUGIN%\scripts\productBuild\productBuild.xml -Dbuilder=%BUILD_BASE_DIR% -DbuildDirectory=%BUILD_BASE_DIR%\eclipse.build -Dbase=%ECLIPSE_BASE% -data %SPELL_GUI_WS% -DpluginPath="%BUILD_BASE_DIR%;%SPELL_GUI_COTS%" -Dverify=true -Dp2.gathering=true -DrepoBaseLocation=%ORBIT_COTS_REPO% -DfeatureList=org.eclipse.equinox.executable -DarchivePrefix=SPELL_GUI_4.0.2 -DJRE=%JRE%

Pause