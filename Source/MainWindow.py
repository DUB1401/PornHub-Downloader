from PyQt6.QtWidgets import (
	QApplication, 
	QCheckBox, 
	QComboBox,
	QGroupBox, 
	QLabel, 
	QMainWindow, 
	QProgressBar, 
	QPushButton, 
	QStyleFactory,
	QTextEdit,
	QVBoxLayout
)

from PyQt6.QtGui import QCursor, QDesktopServices, QMovie, QTextCursor
from Source.QLabelAdvertisement import QLabelAdvertisement
from PyQt6.QtCore import Qt,QSize, QThread, QUrl
from Source.yt_dlp import yt_dlp

import pyperclip
import json
import time
import os
import re

# Обработчик взаимодействий с главным окном.
class MainWindow(QMainWindow):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	# Список поддерживаемых разрешений.
	__Resolutions = ["4096", "2048", "1080", "720", "480", "240"]
	# Поток загрузки видео.
	__DownloadingThread = None
	# Список URL видео.
	__VideoLinks = list()
	# Экземпляр приложения.
	__Application = None
	# Время начала загрузки.
	__StartTime = None
	# Глобальные настройки.
	__Settings = None
	# Словарь важных значений.
	__ComData = None
	# Индекс обрабатываемого видео.
	__VideoIndex = 0

	#==========================================================================================#
	# >>>>> ОБРАБОТЧИКИ СИГНАЛОВ <<<<< #
	#==========================================================================================#

	# Изменяет тему оформления.
	def __ChangeTheme(self):
		# Установка системного стиля и цветовой схемы.
		self.__Application.setStyle(QStyleFactory.keys()[self.__Settings["theme"]])

	# Очищает все данные процесса.
	def __Clear(self):
		self.Input.clear()
		self.Output.clear()
		self.ProgressBar.setValue(0)
		self.__VideoLinks = list()

	# Копирует содержимое псевдоконсоли в буфер обмена.
	def __CopyOutput(self):
		pyperclip.copy(self.Output.toPlainText())

	# Запускает потоковый обработчик загрузки видео.
	def __DownloadVideos(self):
		# Очистка содержимого псевдоконсоли.
		self.Output.clear()
		# Удалить повторяющиеся ссылки.
		self.__RemoveRepeatedLinks()
		# Деактивация управляющих элементов.
		self.Clear.setEnabled(False)
		self.Download.setEnabled(False)
		self.Output.setReadOnly(True)
		self.Paste.setEnabled(False)
		# Получение списка URL видео.
		self.__VideoLinks = list(filter(None, self.Input.toPlainText().strip().split('\n')))
		# Настройка индикатора прогресса.
		self.ProgressBar.setMaximum(len(self.__VideoLinks))
		self.ProgressBar.setValue(0)
		self.ProgressBar.setVisible(True)
		# Запуск загрузчика.
		self.__StartDownloading()

	# Форматирует поле ввода.
	def __FormatInput(self):
		# Получение содержимого поля ввода.
		InputText = self.Input.toPlainText()
		# Разбитие содержимого на отдельные строки.
		InputLines = InputText.split('\n')
		# Обработанные строки.
		FormattedLines = list() 
		# Результирующие строки.
		ResultLines = list()
		# Результирующий текст.
		ResultText = None

		# Для каждой строки.
		for Line in InputLines:
			# Попытаться разбить строку по вхождению протокола.
			Bufer = Line.replace("https", "\nhttps").strip("\n \t")
			# Сохранение разбитых строк.
			FormattedLines += Bufer.split('\n')
		
		# Для каждой обработанной строки.
		for Line in FormattedLines:
			# Очистка строки от аргументов.
			Line = Line.split('&')[0]

			# Если строка соответствует шаблону, то сохранить её.
			if bool(re.match(r"https:\/\/rt\.pornhub\.com\/view_video\.php\?viewkey=\S+\b", Line)) == True:
				ResultLines.append(Line)

		# Построение результирующего текста.
		ResultText = "\n".join(ResultLines) + "\n"

		# Если результирующий текст не содержит символов.
		if ResultText.strip("\n \t") == "":
			# Обнулить результирующий текст.
			ResultText = ""
			# Деактивировать кнопку загрузки.
			self.Download.setEnabled(False)

		elif self.__VideoIndex == 0:
			# Активировать кнопку загрузки.
			self.Download.setEnabled(True)

		# Если текст отличается, то поместить отформатированный список ссылок в поле ввода.
		if ResultText != self.Input.toPlainText():
			self.Input.setText(ResultText)

		# Перемещение каретки в конец поля ввода.
		self.Input.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)

	# Открывает в браузере рекламируемую страницу.
	def __OpenAdvertisement(self):
		QDesktopServices.openUrl(QUrl(self.__Settings["advertisement"]))

	# Открывает в браузере страницу проекта на GitHub.
	def __OpenGitHub(self):
		QDesktopServices.openUrl(QUrl("https://github.com/DUB1401/PornHub-Downloader"))

	# Добавляет ссылку из буфера обмена.
	def __Paste(self):
		self.Input.setText(self.Input.toPlainText() + pyperclip.paste().strip("\n \t") + "\n") 

	# Сохраняет настройку.
	def __SaveSetting(self, Key: str, Value):
		# Обновление значения поля настройки.
		self.__Settings[Key] = Value
		# Копирование настроек.
		Bufer = self.__Settings.copy()

		# Удаление пути к стандартной папке загрузок.
		if Bufer["save-directory"] == os.getcwd() + "\\Downloads":
			Bufer["save-directory"] = ""

		# Сохранение настройки.
		with open("Settings.json", "w", encoding = "utf-8") as FileWrite:
			json.dump(Bufer, FileWrite, ensure_ascii = False, indent = '\t', separators = (",", ": "))

	# Прокручивает псевдоконсоль вниз.
	def __ScrollOutputToEnd(self):
		self.Output.moveCursor(QTextCursor.MoveOperation.End)

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	# Создание группы GUI: реклама.
	def __CreatAdvertisementGroupUI(self):
		# Слой рекламного блока.
		AdvertisementLayout = QVBoxLayout()
		# Установка слоя для элемента QGroupBox.
		self.AdsBox.setLayout(AdvertisementLayout)

		# Создание объекта GUI: рекламная анимация.
		AdvertisementGIF = QMovie("Advertisement.gif")
		AdvertisementGIF.setScaledSize(QSize(180, 260))
		AdvertisementGIF.start()
		
		# Создание объекта GUI: рекламная ссылка.
		Advertisement = QLabelAdvertisement(self)
		Advertisement.clicked.connect(self.__OpenAdvertisement)
		Advertisement.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		Advertisement.setMovie(AdvertisementGIF)
		
		# Добавление объекта GUI в слой.
		AdvertisementLayout.addWidget(Advertisement)

	# Создание базовых элементов GUI.
	def __CreateBasicUI(self):

		# Создание объекта GUI: контейнер рекламы.
		self.AdsBox = QGroupBox(self)
		self.AdsBox.move(870, 170)
		self.AdsBox.resize(200, 300)
		self.AdsBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.AdsBox.setTitle("📰 Advertisement")

		# Создание объекта GUI: кнока очистки вывода.
		self.Clear = QPushButton(self)
		self.Clear.clicked.connect(self.__Clear)
		self.Clear.move(870, 590)
		self.Clear.resize(200, 40)
		self.Clear.setText("🧹 Clear")

		# Создание объекта GUI: кнока копирования вывода.
		self.Copy = QPushButton(self)
		self.Copy.clicked.connect(self.__CopyOutput)
		self.Copy.move(870, 540)
		self.Copy.resize(200, 40)
		self.Copy.setText("📋 Copy output")

		# Создание объекта GUI: подпись защиты прав.
		self.Copyright = QLabel(self)
		self.Copyright.setText(self.__ComData["copyright"])
		self.Copyright.move(10, 690)
		self.Copyright.adjustSize()

		# Создание объекта GUI: кнока загрузки.
		self.Download = QPushButton(self)
		self.Download.clicked.connect(self.__DownloadVideos)
		self.Download.move(870, 640)
		self.Download.resize(200, 40)
		self.Download.setEnabled(False)
		self.Download.setText("⬇ Download")

		# Создание объекта GUI: поле ввода ссылок на видео.
		self.Input = QTextEdit(self)
		self.Input.move(10, 10)
		self.Input.resize(850, 420)
		self.Input.setPlaceholderText("Paste here links to videos")
		self.Input.textChanged.connect(self.__FormatInput)

		# Создание объекта GUI: ссылка на GitHub.
		self.Link = QLabel(self)
		self.Link.linkActivated.connect(self.__OpenGitHub)
		self.Link.move(1030, 690)
		self.Link.setText("<a href=\"https://github.com/DUB1401/PornHub-Downloader\">GitHub</a>")
		self.Link.adjustSize()

		# Создание объекта GUI: поле псевдоконсольного вывода.
		self.Output = QTextEdit(self)
		self.Output.move(10, 490)
		self.Output.resize(850, 190)
		self.Output.setReadOnly(True)
		self.Output.setPlaceholderText("Output logs")
		self.Output.textChanged.connect(self.__ScrollOutputToEnd)

		# Создание объекта GUI: кнока добавления ссылки в очередь.
		self.Paste = QPushButton(self)
		self.Paste.clicked.connect(self.__Paste)
		self.Paste.move(870, 490)
		self.Paste.resize(200, 40)
		self.Paste.setText("📖 Paste link")

		# Создание объекта GUI: индикатор прогресса.
		self.ProgressBar = QProgressBar(self)
		self.ProgressBar.move(10, 450)
		self.ProgressBar.resize(850, 20)
		self.ProgressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.ProgressBar.setValue(0)

		# Создание объекта GUI: контейнер настроек.
		self.SettingsBox = QGroupBox(self)
		self.SettingsBox.move(870, 10)
		self.SettingsBox.resize(200, 160)
		self.SettingsBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.SettingsBox.setTitle("🔧 Settings")

	# Создание группы GUI: настройки.
	def __CreateSettingsGroupUI(self):
		# Слой настроек.
		SettingsLayout = QVBoxLayout()
		# Установка слоя для элемента QGroupBox.
		self.SettingsBox.setLayout(SettingsLayout)

		#---> Создание объектов GUI.
		#==========================================================================================#

		# Создание объекта GUI: заголовок выбора качества.
		CualityTitle = QLabel(self)
		CualityTitle.setText("Cuality:")
		CualityTitle.adjustSize()

		# Создание объекта GUI: селектор качества.
		CualitySelecter = QComboBox(self)
		CualitySelecter.addItems(["4K", "2K", "1080", "720", "480", "240"])
		CualitySelecter.setCurrentIndex(self.__Settings["cuality"])
		CualitySelecter.currentIndexChanged.connect(lambda: self.__SaveSetting("cuality", CualitySelecter.currentIndex()))
		CualitySelecter.resize(180, 40)
		CualitySelecter.setToolTip("Resolution of the downloaded video.")

		# Создание объекта GUI: заголовок выбора темы.
		ThemeTitle = QLabel(self)
		ThemeTitle.setText("Theme:")
		ThemeTitle.adjustSize()

		# Создание объекта GUI: селектор темы.
		ThemeSelecter = QComboBox(self)
		ThemeSelecter.addItems(QStyleFactory.keys())
		ThemeSelecter.setCurrentIndex(self.__Settings["theme"])
		ThemeSelecter.currentIndexChanged.connect(lambda: self.__SaveSetting("theme", ThemeSelecter.currentIndex()))
		ThemeSelecter.currentIndexChanged.connect(self.__ChangeTheme)
		ThemeSelecter.resize(180, 20)
		ThemeSelecter.setToolTip("Sets the style of the program window.")

		# Создание объекта GUI: флаговая кнопка включения сортировки по моделям.
		SortByModel = QCheckBox(self)
		SortByModel.clicked.connect(lambda: self.__SaveSetting("sort-by-models", SortByModel.isChecked()))
		SortByModel.setChecked(self.__Settings["sort-by-models"])
		SortByModel.setText("Sort by models")
		SortByModel.setToolTip("Sorting videos into the folders by uploader nickname.")
		SortByModel.adjustSize()
		
		#---> Добавление объектов GUI в слой.
		#==========================================================================================#
		SettingsLayout.addWidget(SortByModel)
		SettingsLayout.addWidget(ThemeTitle)
		SettingsLayout.addWidget(ThemeSelecter)
		SettingsLayout.addWidget(CualityTitle)
		SettingsLayout.addWidget(CualitySelecter)
		SettingsLayout.addStretch()

	# Обрабатывает завершение загрузки видео.
	def __EndDownloading(self, ExitCode: int):
		# Инкремент индекса загружаемого видео.
		self.__VideoIndex += 1
		# Увеличение процента заполнение в индикаторе прогресса.
		self.ProgressBar.setValue(self.__VideoIndex)

		# Если загрузка завершилась успешно, то вывести в псевдоконсоль время выполнения, иначе вывести ошибку.
		if ExitCode == 0:
			self.Print("<b style=\"color: green;\">Done!</b> (" + self.__FormatExecutionTime(round(float(time.time() - self.__StartTime), 2)) + ")", True)

		else:
			self.Print("<b style=\"color: red;\">Error!</b> See CMD output for more information.", True)

		# Удаление первого в очереди URL.
		self.Input.setText('\n'.join(self.Input.toPlainText().split('\n')[1:]))

		# Если остались незагруженные видео.
		if self.__VideoIndex < len(self.__VideoLinks):
			# Начать загрузку следующего видео.
			self.__StartDownloading()

		else:
			# Вывод в псевдоконсоль: работа завершена.
			self.Print("Complete.")
			# Активация управляющих элементов.
			self.Clear.setEnabled(True)
			self.Download.setEnabled(True)
			self.Output.setReadOnly(False)
			self.Paste.setEnabled(True)
			# Обнуление индекса загружаемого видео.
			self.__VideoIndex = 0
			# Очистка поля ввода.
			self.Input.setText("")

	# Форматирует время выполнения задачи.
	def __FormatExecutionTime(self, ExecutionTime: float) -> str:
		# Результат форматирования.
		Result = ""
		# Получение количества прошедших минут.
		ElapsedMinutes = int(ExecutionTime / 60.0)

		# Если прошло больше минуты.
		if ElapsedMinutes > 0:
			# Добавление количества прошедших минут в формат.
			Result += str(ElapsedMinutes) + " minutes "
			# Вычисление оставшихся секунд.
			ElapsedSeconds = round(ExecutionTime % 60.0, 2)
			# Добавление количества оставшихся секунд в формат.
			Result += str(ElapsedSeconds) + " seconds"

		else:
			# Форматирование прошедших секунд.
			Result += str(ExecutionTime) + " seconds"

		return Result

	# Удаляет повторяющиеся ссылки.
	def __RemoveRepeatedLinks(self):
		# Получение содержимого поля ввода.
		InputText = self.Input.toPlainText()
		# Разбитие содержимого на отдельные строки.
		InputLines = InputText.split('\n')
		# Удаление дубликатов ссылок.
		ResultLines = [*set(InputLines)]

		# Если количество ссылок отличается от изначального.
		if len(InputLines) != len(ResultLines):
			# Построение результирующего текста.
			ResultText = "\n".join(ResultLines) + "\n"
			# Поместить отсортированный список ссылок в поле ввода.
			self.Input.setText(ResultText)
			# Вычисление количества удалённых повторов.
			RepeatedLinksCount = len(InputLines) - len(ResultLines)
			# Вывод в псевдоконсоль: количество удалённых повторов.
			self.Print("<b>Removed identical links count:</b> " + str(RepeatedLinksCount), True)

	# Обрабатывает начало загрузки видео.
	def __StartDownloading(self):
		# Директория загрузки.
		SaveDirectory = self.__Settings["save-directory"]

		# Сохранение времени начала загрузки.
		self.__StartTime = time.time()

		# Если остались незагруженные видео.
		if self.__VideoIndex < len(self.__VideoLinks):
			# Текущая ссылка.
			CurrentLink = self.__VideoLinks[self.__VideoIndex]
			# Вывод в псевдоконсоль: начало загрузки.
			self.Print("<b>Downloading: </b>" + str(self.__VideoIndex + 1) + " / " + str(len(self.__VideoLinks)))
			# Вывод в псевдоконсоль: URL текущей задачи.
			self.Print("<b>Current task:</b> <i>" + self.__VideoLinks[self.__VideoIndex] + "</i>")
			# Настройка и запуск обработчика библиотеки в отдельном потоке.
			self.Subprocess = yt_dlp(SaveDirectory, CurrentLink, self.__Settings["sort-by-models"], self.__Resolutions[self.__Settings["cuality"]])
			self.Subprocess.moveToThread(self.__DownloadingThread)
			self.__DownloadingThread.quit()
			self.__DownloadingThread.started.connect(self.Subprocess.run)
			self.Subprocess.finished.connect(self.__EndDownloading)
			self.Subprocess.finished.connect(self.__DownloadingThread.quit)
			self.__DownloadingThread.start()

	# Конструктор: задаёт экземпляр приложения, словарь важных значений и глобальные настройки.
	def __init__(self, Application: QApplication, ComData: dict, Settings: dict):
		# Обеспечение доступа к оригиналам наследованных методов.
		super().__init__()

		#---> Генерация свойств.
		#==========================================================================================#
		self.__ComData = ComData
		self.__Settings = Settings
		self.__DownloadingThread = QThread()
		self.__Application = Application

		#---> Инициализация графического интерфейса.
		#==========================================================================================#

		# Настройка окна.
		self.setFixedSize(1080, 720)
		self.setWindowTitle("PornHub Downloader v" + ComData["version"])

		# Создание базовых элементов и групп GUI.
		self.__CreateBasicUI()
		self.__CreateSettingsGroupUI()

		# Если включено отображение рекламы.
		if self.__Settings["advertisement"] != "" and self.__Settings["advertisement"] != None and os.path.exists("Advertisement.gif"):
			# Генерация рекламного блока.
			self.__CreatAdvertisementGroupUI()

		else:
			# Отключение видимости рекламного блока.
			self.AdsBox.setVisible(False)

		# Если включён режим отладки, то добавить две тестовые ссылки в поле ввода.
		if self.__Settings["debug"] == True:
			self.Input.setText("https://rt.pornhub.com/view_video.php?viewkey=ph5c7ad8fa8b178\nhttps://rt.pornhub.com/view_video.php?viewkey=ph5d302376d91be\n")

	# Отправляет сообщение в псевдоконсоль.
	def Print(self, Message: str, Separator: bool = False):
		# Содержимое псевдоконсоли.
		Text = None

		# Если псевдоконсоль пуста, то задать пустой текст (исправляет наличие пустой строки).
		if self.Output.toPlainText() == "":
			Text = ""

		else:
			Text = self.Output.toHtml()

		# Если указано аргументами, то добавить разделитель после сообщения.
		if Separator == True:
			Message += "<br>=========================================================================================="

		# Добавление сообщения в конец.
		self.Output.setHtml(Text + Message)