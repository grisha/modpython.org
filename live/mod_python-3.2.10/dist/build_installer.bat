@echo off
rem Copyright 2004 Apache Software Foundation
rem  
rem  Licensed under the Apache License, Version 2.0 (the "License");
rem  you may not use this file except in compliance with the License.
rem  You may obtain a copy of the License at
rem  
rem      http://www.apache.org/licenses/LICENSE-2.0
rem  
rem  Unless required by applicable law or agreed to in writing, software
rem  distributed under the License is distributed on an "AS IS" BASIS,
rem  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
rem  See the License for the specific language governing permissions and
rem  limitations under the License.
rem  
rem Originally developed by Gregory Trubetskoy.
rem  
rem $Id: build_installer.bat 345063 2005-11-16 17:16:41Z nlehuen $
rem
rem This script builds the installer for Windows

rem Test for APACHESRC
if "%APACHESRC%"=="" GOTO NOAPACHESRC
if not exist "%APACHESRC%\include" GOTO BADAPACHESRC

rem Cleanup
rmdir /s /q build
del ..\src\*.obj ..\src\*.lib ..\src\*.exp ..\src\*.res

rem Build
python setup.py.in bdist_wininst --install-script win32_postinstall.py

rem Compress the installer if possible
upx.exe --no-color --no-progress --best dist\*.exe
GOTO END

:BADAPACHESRC
echo Currently APACHESRC points to %APACHESRC%
echo This value seems wrong as we could not find a proper Apache installation here.

:NOAPACHESRC
echo Please set the APACHESRC variable to point to your Apache setup
echo E.g. set APACHESRC=c:\apache
echo This can be a binary distribution, no need for the Apache sources.
GOTO END

:END
