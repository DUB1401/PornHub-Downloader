:: Переход в директорию проекта.
cd ..\

:: Сборка приложения.
pyinstaller --distpath %~dp0\Release --i icon.ico --version-file Build\metadata.txt --onefile "PornHub Downloader.py"

:: Копирование в директорию сборки необходимых компонентов приложения.
xcopy /Y /I yt-dlp Build\Release\yt-dlp
xcopy /Y Advertisement.gif Build\Release
xcopy /Y Settings.json Build\Release
xcopy /Y icon.ico Build\Release

:: Удаление файлов сборки приложения.
rmdir /q /s "Build\PornHub Downloader"