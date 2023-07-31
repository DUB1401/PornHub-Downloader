from PyQt6.QtCore import QObject, pyqtSignal

import subprocess
import json
import os

# Потоковый обработчик взаимодейтсвий с библиотекой pornhub_dl.
class yt_dlp(QObject):

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	# Текущая директория.
	__CurrentDirectory = None
	# Сигнал: завершение потока. Содержит: завершающий код вызова библиотеки.
	finished = pyqtSignal(int)
	# Состояние: требуется ли сортировать видео по никам загрузивших.
	__SortByUploader = None
	# Директория сохранения.
	__SaveDirectory = None
	# Дамп данных видео.
	__Dump = None
	# Ссылка на видео.
	__Link = None

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	# Конструктор: задаёт команду для выполнения.
	def __init__(self, SaveDirectory: str, Link: str, SortByUploader: bool):
		# Обеспечение доступа к оригиналам наследованных методов.
		super().__init__()

		#---> Генерация свойств.
		#==========================================================================================#
		self.__CurrentDirectory = os.getcwd()
		self.__SaveDirectory = SaveDirectory
		self.__Link = Link
		self.__SortByUploader = SortByUploader

	# Возвращает словарь описания предварительного процессирования yt-dlp.
	def dump(self) -> dict:
		# Получение дампа через вывод yt-dlp.
		self.__Dump = json.loads(subprocess.getoutput(f"{self.__CurrentDirectory}\\yt-dlp\\yt-dlp --dump-json {self.__Link}"))

		return self.__Dump

	# Запускает выполнение команды.
	def run(self):
		# Дампирование видео.
		self.dump()
		# Получение имени файла и расширения.
		Filename = self.__Dump["filename"]
		# Получение имени загрузившего для сортировки.
		Uploader = "\\" + self.__Dump["uploader"]

		# Если сортировка отключена, обнулить загрузившего.
		if self.__SortByUploader == False:
			Uploader = ""

		# Выполнение команды.
		ExitCode = os.system(f"{self.__CurrentDirectory}\\yt-dlp\\yt-dlp -o \"{self.__SaveDirectory}{Uploader}\\{Filename}\" {self.__Link}")
		# Генерация сигнала с завершающим кодом приложения.
		self.finished.emit(ExitCode)