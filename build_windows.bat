@echo off
echo Building Web Cloner for Windows...

rem Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

rem Install dependencies
pip install -r requirements.txt

rem Build with PyInstaller
pyinstaller --name="Web Cloner" ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="icon.ico;." ^
            --collect-all customtkinter ^
            web-cloner.py

echo Build completed. The executable is located in the dist\ folder

pause 