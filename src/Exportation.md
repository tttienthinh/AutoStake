# Windows

pyinstaller -y --add-binary "drivers\*.exe;drivers\" --add-data "data/*;data/" main.py