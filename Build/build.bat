:: Переход в директорию проекта.
cd ..\

:: Сборка приложения.
pyinstaller --distpath %~dp0\Release --i icon.ico --version-file Build\metadata.txt --onefile "PornHub Downloader.py"

:: Копирование в директорию сборки необходимых компонентов приложения.
xcopy /Y /I pornhub_dl Build\Release\pornhub_dl
xcopy /Y Advertisement.gif Build\Release
xcopy /Y Settings.json Build\Release
xcopy /Y icon.ico Build\Release

:: Удаление файлов сборки приложения.
rmdir /q /s "Build\PornHub Downloader"

:: Переход в директорию библиотеки.
cd pornhub_dl

:: Сборка библиотеки.
pyinstaller --distpath %~dp0\Release\pornhub_dl --onefile --collect-all pyfiglet "pornhub_dl.py"

:: Переход в директорию проекта.
cd ..\

:: Удаление ненужных файлов библиотеки.
del /q Build\Release\pornhub_dl\lib_pornhub.py
del /q Build\Release\pornhub_dl\pornhub_dl.py
del /q Build\Release\pornhub_dl\pornhub_dl.py
del /q Build\Release\pornhub_dl\pornhub_dl.spec
del /q Build\Release\pornhub_dl\requirements.txt
