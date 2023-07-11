# PornHub Downloader
**PornHub Downloader** – это приложение с графическим интерфейсом для массовой загрузки видеороликов с [PornHub](https://www.pornhub.com/), поддерживающее сортировку по моделям.

## Порядок установки и использования
1. Загрузить последний релиз. Распаковать.
2. Установить Python версии не старше 3.10. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [pyperclip](https://github.com/asweigart/pyperclip), [pyfiglet](https://github.com/pwaller/pyfiglet), [requests](https://github.com/psf/requests), [pyqt6](https://www.riverbankcomputing.com/software/pyqt/), [lxml](https://github.com/lxml/lxml), [tqdm](https://github.com/tqdm/tqdm).
```
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
4. Запустить _PornHub Downloader.py_.
5. Вставить в поле ввода список ссылок на видео так, чтобы каждая занимала одну строку, и нажать кнопку загрузки.
6. Дождаться загрузки видео в  папку _Downloads_, в директории скрипта.

# Скриншот
![2023-07-09_17-46-34](https://github.com/DUB1401/PornHub-Downloader/assets/40277356/23716486-985f-40ec-962c-04b42bc1af1f)

# Благодарность
* [@yt-dlp](https://github.com/yt-dlp) – библиотека загрузки потокового видео.
* [@tnt2402](https://github.com/tnt2402) – консольная имплементация [yt-dlp](https://github.com/yt-dlp/yt-dlp) для загрузки видеороликов с [PornHub](https://www.pornhub.com/).

_Copyright © DUB1401. 2023._