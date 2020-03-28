pyinstaller -F start.py
copy dist\start.exe .\start.exe
rmdir /s/q build
rmdir /s/q dist
del start.spec