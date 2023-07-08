from genericpath import isdir
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

from PyQt6.QtCore import (
	QObject, 
	Qt,
	QThread, 
	QUrl,
	pyqtSignal
)

from PyQt6.QtGui import QDesktopServices

import pyperclip
import shutil
import json
import os

# Потоковый обработчик взаимодейтсвий с библиотекой pornhub_dl.
class PornhubLibSubprocess(QObject):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	# Сигнал: завершение потока. Содержит: завершающий код вызова библиотеки.
	finished = pyqtSignal(int)
	# Исполняемая команда.
	__Command = None

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	# Конструктор: задаёт команду для выполнения.
	def __init__(self, Command: str):
		# 
		super().__init__()

		#---> Генерация свойств.
		#==========================================================================================#
		self.__Command = Command

	# Запускает выполнение команды.
	def run(self):
		# Выполнение команды.
		ExitCode = os.system(self.__Command)
		# Генерация сигнала с завершающим кодом приложения.
		self.finished.emit(ExitCode)

# Обработчик взаимодействий с главным окном.
class MainWindow(QMainWindow):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	# Поток загрузки видео.
	__DownloadingThread = None
	# Список URL видео.
	__VideoLinks = list()
	# Индекс обрабатываемого видео.
	__VideoIndex = None
	# Глобальные настройки.
	__Settings = None
	# Словарь важных значений.
	__ComData = None
	# Экземпляр приложения.
	__Application = None

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
		self.Output.setText("")
		# Деактивация управляющих элементов.
		self.Clear.setEnabled(False)
		self.Download.setEnabled(False)
		self.Output.setReadOnly(True)
		self.Paste.setEnabled(False)
		# Получение списка URL видео.
		self.__VideoLinks = list(filter(None, self.Input.toPlainText().strip().split('\n')))
		# Текущая директория.
		CurrentDirectory = os.getcwd()
		# Обнуление индекса загружаемого видео.
		self.__VideoIndex = 0
		# Установка текущей директории для библиотеки.
		os.chdir(CurrentDirectory + "\\pornhub_dl")
		# Настройка индикатора прогресса.
		self.ProgressBar.setMaximum(len(self.__VideoLinks))
		self.ProgressBar.setValue(0)
		self.ProgressBar.setVisible(True)
		# Запуск загрузчика.
		self.__StartDownloading()

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
		self.Download.setText("⬇ Download")

		# Создание объекта GUI: поле ввода ссылок на видео.
		self.Input = QTextEdit(self)
		self.Input.move(10, 10)
		self.Input.resize(850, 420)
		self.Input.setPlaceholderText("Paste here links to videos or press button...")

		# Создание объекта GUI: ссылка на GitHub.
		self.Link = QLabel(self)
		self.Link.linkActivated.connect(self.__OpenGitHub)
		self.Link.move(1030, 690)
		self.Link.setText("<a href=\"http://stackoverflow.com/\">GitHub</a>")
		self.Link.adjustSize()

		# Создание объекта GUI: поле псевдоконсольного вывода.
		self.Output = QTextEdit(self)
		self.Output.move(10, 490)
		self.Output.resize(850, 190)
		self.Output.setReadOnly(True)
		self.Output.setPlaceholderText("Output logs...")

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
		self.SettingsBox.move(870, 0)
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
	def __EndDownloading(self):
		# Инкремент индекса загружаемого видео.
		self.__VideoIndex += 1
		# Текущая директория.
		CurrentDirectory = os.getcwd()
		# Увеличение процента заполнение в индикаторе прогресса.
		self.ProgressBar.setValue(self.__VideoIndex)
		# Вывод в псевдоконсоль: разделитель.
		self.Output.setText(self.Output.toPlainText() + "==========================================================================================\n")
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
			self.Output.setText(self.Output.toPlainText() + "Complete.\n")
			# Активация управляющих элементов.
			self.Clear.setEnabled(True)
			self.Download.setEnabled(True)
			self.Output.setReadOnly(False)
			self.Paste.setEnabled(True)
			# Очистка поля ввода.
			self.Input.setText("")

	# Обрабатывает начало загрузки видео.
	def __StartDownloading(self):
		# Текущая директория.
		CurrentDirectory = os.getcwd()
		# Директория загрузки.
		SaveDirectory = self.__Settings["save-directory"]

		# Если остались незагруженные видео.
		if self.__VideoIndex < len(self.__VideoLinks):
			# Текущая ссылка.
			CurrentLink = self.__VideoLinks[self.__VideoIndex]
			# Вывод в псевдоконсоль: начало загрузки.
			self.Output.setText(self.Output.toPlainText() + "Downloading: " + str(self.__VideoIndex + 1) + " / " + str(len(self.__VideoLinks)) + "\n")
			# Вывод в псевдоконсоль: название видео.
			self.Output.setText(self.Output.toPlainText() + "Current task: " + self.__VideoLinks[self.__VideoIndex] + "\n")
			# Настройка и запуск обработчика библиотеки в отдельном потоке.
			self.Subprocess = PornhubLibSubprocess(f"{CurrentDirectory}/pornhub_dl.py --url {CurrentLink} --dir \"{SaveDirectory}\"")
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

	# Конструктор.
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