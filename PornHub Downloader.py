from PyQt6.QtWidgets import QApplication, QStyleFactory
from Source.MainWindow import MainWindow
from PyQt6 import QtGui

import ctypes
import json
import sys
import os

#==========================================================================================#
# >>>>> ПРОВЕРКА ВЕРСИИ PYTHON <<<<< #
#==========================================================================================#

# Минимальная требуемая версия Python.
PythonMinimalVersion = (3, 10)
# Проверка соответствия.
if sys.version_info < PythonMinimalVersion:
	sys.exit("Python %s.%s or later is required.\n" % PythonMinimalVersion)

#==========================================================================================#
# >>>>> ЧТЕНИЕ НАСТРОЕК <<<<< #
#==========================================================================================#

# Глобальные настройки.
Settings = {
	"sort-by-models": False,
	"save-directory": "",
	"theme": 2,
	"debug": False
}
# Словарь важных значений.
ComData = {
	"version": "1.1.0",
	"copyright": "Copyright © 2023. DUB1401."
}

# Проверка доступности файла настроек.
if os.path.exists("Settings.json"):

	# Открытие файла настроек.
	with open("Settings.json", encoding = "utf-8") as FileRead:
		# Чтение настроек.
		Settings = json.load(FileRead)

		# Если директория для загрузки не указана.
		if Settings["save-directory"] == "":
			# Формирование пути.
			Settings["save-directory"] = os.getcwd() + "\\Downloads"

			# Если стандартной папки не существует, то создать.
			if os.path.exists("Downloads") == False:
				os.makedirs("Downloads")

else:
	# Выбро исключения.
	raise Exception("Settings.json file not found.")

# Если не включён режим отладки, то свернуть консоль при запуске.
if Settings["debug"] == False:
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА <<<<< #
#==========================================================================================#

# Создание экземпляра приложения.
Application = QApplication(sys.argv)
# Установка системного стиля и цветовой схемы.
Application.setStyle(QStyleFactory.keys()[Settings["theme"]])
# Установка икноки.
Application.setWindowIcon(QtGui.QIcon("icon.ico"))
# Открытие главного окна.
MainWindowObject = MainWindow(Application, ComData, Settings)
MainWindowObject.show()
# Запуск обработки приложения.
Application.exec()

# Завершение работы скрипта.
sys.exit(Application.exit())
