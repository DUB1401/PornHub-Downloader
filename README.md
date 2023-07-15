# PornHub Downloader
**PornHub Downloader** – это приложение с графическим интерфейсом для массовой загрузки видеороликов с [PornHub](https://www.pornhub.com/), поддерживающее сортировку по моделям.

## Порядок установки и использования | Исполняемый файл Windows
1. Загрузить последний релиз исполняемой версии. Распаковать.
2. Запустить _PornHub Downloader.exe_. Вставить в поле ввода список ссылок на видео и нажать кнопку загрузки.
3. Дождаться скачивания видео в  папку _Downloads_, в директории скрипта.

## Порядок установки и использования | Скрипт Python
1. Загрузить последний релиз скрипта. Распаковать.
2. Установить Python версии не старше 3.10. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [pyinstaller](https://github.com/pyinstaller/pyinstaller), [pyperclip](https://github.com/asweigart/pyperclip), [pyfiglet](https://github.com/pwaller/pyfiglet), [requests](https://github.com/psf/requests), [pyqt6](https://www.riverbankcomputing.com/software/pyqt/), [lxml](https://github.com/lxml/lxml), [tqdm](https://github.com/tqdm/tqdm).
```
pip install pyinstaller
pip install pyperclip
pip install pyfiglet
pip install requests
pip install pyqt6
pip install lxml
pip install tqdm
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. Запустить _PornHub Downloader.py_. Вставить в поле ввода список ссылок на видео и нажать кнопку загрузки.
5. Дождаться скачивания видео в  папку _Downloads_, в директории скрипта.

# Скриншот
![2023-07-15_13-16-38](https://github.com/DUB1401/PornHub-Downloader/assets/40277356/77ce1874-87f0-4f0c-9e1f-8ce8633a2fea)

# Сборка
1. Подготовить скрипт Python к работе согласно инструкции из порядка установки и использования.
2. Перейти в папку _Build_, внутри директории скрипта.
3. Запустить файл _build.bat_ и дождаться завершения работы.
4. Исполняемая версия будет помещена по адресу _Build/Release_ вместе со всеми зависимостями.

# Благодарность
* [@yt-dlp](https://github.com/yt-dlp) – библиотека загрузки потокового видео.
* [@tnt2402](https://github.com/tnt2402) – консольная имплементация [yt-dlp](https://github.com/yt-dlp/yt-dlp) для загрузки видеороликов с [PornHub](https://www.pornhub.com/).

_Copyright © DUB1401. 2023._