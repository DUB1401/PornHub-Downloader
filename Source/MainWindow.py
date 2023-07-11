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

from Source.pornhub_dl import pornhub_dl
from PyQt6.QtGui import QDesktopServices, QTextCursor
from PyQt6.QtCore import Qt,QThread, QUrl

import pyperclip
import shutil
import json
import time
import os
import re

# Обработчик взаимодействий с главным окном.
class MainWindow(QMainWindow):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

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
		# Текущая директория.
		CurrentDirectory = os.getcwd()
		# Установка текущей директории для библиотеки.
		os.chdir(CurrentDirectory + "\\pornhub_dl")
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
		Bufer = self.__Settings

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

	# Создание базовых элементов GUI.
	def __CreateBasicUI(self):

		# Создание объекта GUI: контейнер рекламы.
		self.AdsBlock = QGroupBox(self)
		self.AdsBlock.move(870, 130)
		self.AdsBlock.resize(200, 300)
		self.AdsBlock.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.AdsBlock.setTitle("📰 Advertisement")

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
		self.SettingsBox.resize(200, 120)
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
		
		# Создание объекта GUI: флаговая кнопка включения сортировки по моделям.
		SortByModel = QCheckBox(self)
		SortByModel.clicked.connect(lambda: self.__SaveSetting("sort-by-models", SortByModel.isChecked()))
		SortByModel.setText("Sort by models")
		SortByModel.adjustSize()
		SortByModel.setChecked(self.__Settings["sort-by-models"])
		
		#---> Добавление объектов GUI в слой.
		#==========================================================================================#
		SettingsLayout.addWidget(SortByModel)
		SettingsLayout.addWidget(ThemeTitle)
		SettingsLayout.addWidget(ThemeSelecter)
		SettingsLayout.addStretch()

	# Обрабатывает завершение загрузки видео.
	def __EndDownloading(self, ExitCode: int):
		# Инкремент индекса загружаемого видео.
		self.__VideoIndex += 1
		# Текущая директория.
		CurrentDirectory = os.getcwd()
		# Увеличение процента заполнение в индикаторе прогресса.
		self.ProgressBar.setValue(self.__VideoIndex)

		# Если загрузка завершилась успешно, то вывести в псевдоконсоль время выполнения, иначе вывести ошибку.
		if ExitCode == 0:
			self.Print("<b style=\"color: green;\">Done!</b> (" + str(round(float(time.time() - self.__StartTime), 2)) + " seconds)", True)

		else:
			self.Print("<b style=\"color: red;\">Error!</b> See CMD output for more information.", True)

		# Структурировать загруженные видео.
		self.__StructurizateDownloads()
		# Удаление первого в очереди URL.
		self.Input.setText('\n'.join(self.Input.toPlainText().split('\n')[1:]))

		# Если остались незагруженные видео.
		if self.__VideoIndex < len(self.__VideoLinks):
			# Начать загрузку следующего видео.
			self.__StartDownloading()

		else:
			# Установка текущей директории для библиотеки.
			os.chdir(CurrentDirectory.replace("\\pornhub_dl", ""))
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
		# Текущая директория.
		CurrentDirectory = os.getcwd()
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
			self.Subprocess = pornhub_dl(f"{CurrentDirectory}\\pornhub_dl.py --url {CurrentLink} --dir \"{SaveDirectory}\"")
			self.Subprocess.moveToThread(self.__DownloadingThread)
			self.__DownloadingThread.quit()
			self.__DownloadingThread.started.connect(self.Subprocess.run)
			self.Subprocess.finished.connect(self.__EndDownloading)
			self.Subprocess.finished.connect(self.__DownloadingThread.quit)
			self.__DownloadingThread.start()

	# Структурирует загруженные видео.
	def __StructurizateDownloads(self):
		# Получение списка папок в директории models.
		FoldersList = os.listdir(self.__Settings["save-directory"] + "\\model")

		# Если включена сортировка по моделям.
		if self.__Settings["sort-by-models"] == True:
			
			# Каждую папку переместить в целевую директорию.
			for Folder in FoldersList:

				try:
					shutil.move(self.__Settings["save-directory"] + "\\model\\" + Folder, self.__Settings["save-directory"])

				except shutil.Error:
					pass

			# Удалить исходную директорию с файлами.
			shutil.rmtree(self.__Settings["save-directory"] + "\\model")

		else:
			
			# Для каждой папки с названием модели.
			for Folder in FoldersList:
				# Получение списка файлов в директории модели.
				FilesList = os.listdir(self.__Settings["save-directory"] + "\\model\\" + Folder)

				# Каждый файл переместить в целевую директорию.
				for File in FilesList:

					try:
						shutil.move(self.__Settings["save-directory"] + "\\model\\" + Folder + "\\" + File, self.__Settings["save-directory"])

					except shutil.Error:
						pass

			# Удалить исходную директорию с файлами.
			shutil.rmtree(self.__Settings["save-directory"] + "\\model")

	# Конструктор: задаёт экземпляр приложения, словарь важных значений и глобальные настройки.
	def __init__(self, Application: QApplication, ComData: dict, Settings: dict):
		# 
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

		# Отключение блока рекламы.
		self.AdsBlock.setVisible(False)

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