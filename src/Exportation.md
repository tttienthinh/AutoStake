# Windows
(pyinstaller)

pyinstaller -y --add-binary "drivers\*.exe;drivers\" --add-data "data/*;data/" --icon=Binance_Logo.ico AutoStake.py

# Mac 
(py2app)

py2applet --make-setup AutoStake.py