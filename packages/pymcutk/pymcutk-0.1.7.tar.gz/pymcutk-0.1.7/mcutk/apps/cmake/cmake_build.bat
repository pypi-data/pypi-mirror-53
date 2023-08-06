@echo off
cd /d %1

REM clean projects
if exist CMakeFiles (
    rd /s /Q CMakeFiles
)
if exist %2 (
    rd /s /Q %2
)
del /s /Q /F Makefile cmake_install.cmake CMakeCache.txt

cmake -DCMAKE_TOOLCHAIN_FILE=%3 -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=%2 .

if not %errorlevel% == 0 (exit /b %errorlevel%)

mingw32-make -C . -j4

exit /b %errorlevel%
