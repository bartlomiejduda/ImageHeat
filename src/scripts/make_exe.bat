
:: BAT script for making exe file
:: Created on 11.11.2024 by Bartlomiej Duda


@ECHO OFF
if exist dist (rd /s /q dist)
if exist build (rd /s /q build)
if exist build_final (rd /s /q build_final)


echo Activating venv...
CALL .\venv\Scripts\activate.bat

echo Executing cxfreeze...
python setup.py build build_exe


if exist __pycache__ (rd /s /q __pycache__)

echo Copying files...
set BUILD_PATH=.\build_final\ImageHeat
set TARGET_SRC_PATH=%BUILD_PATH%\lib\src
copy .\src\data\docs\readme.txt %BUILD_PATH%\readme.txt
copy .\LICENSE %BUILD_PATH%\LICENSE
mkdir %BUILD_PATH%\data\img
copy .\src\data\img\heat_icon.ico %BUILD_PATH%\data\img\heat_icon.ico
copy .\src\data\img\preview_not_supported.png %BUILD_PATH%\data\img\preview_not_supported.png
xcopy /s .\src\data\lang %BUILD_PATH%\data\lang\
if exist %TARGET_SRC_PATH%\log.txt (del %TARGET_SRC_PATH%\log.txt)
if exist %TARGET_SRC_PATH%\config.ini (del %TARGET_SRC_PATH%\config.ini)


echo BUILD SUCCESSFUL!
