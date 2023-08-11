import ctypes
import locale
import sys 

# Словарь локализаций.
LOCALES = {
	"DE": [
		"Werbung",
		"Klar",
		"Copy output",
		"Ausgabe kopieren",
		"Fügen sie hier links zu videos ein",
		"Ausgabeprotokolle",
		"Links einfügen",
		"Einstellung",
		"Qualität",
		"Auflösung des heruntergeladenen videos.",
		"Thema",
		"Stil des programmfensters.",
		"Sortieren nach modellen"
	],
	"EN": [
		"Advertisement",
		"Clear",
		"Copy output",
		"Download",
		"Paste here links to videos",
		"Output logs",
		"Paste links",
		"Settings",
		"Cuality",
		"Resolution of the downloaded video.",
		"Theme",
		"Style of the program window.",
		"Sort by models"
	],
	"PL": [
		"Reklama",
		"Oczyścić",
		"Kopiuj dzienniki",
		"Pozbyć się",
		"Wstaw tutaj linki do filmów",
		"Logi",
		"Wstaw linki",
		"Konfiguracja",
		"Jakość",
		"Rozdzielczość pobieranego wideo.",
		"Temat",
		"Styl okna programu.",
		"Sortuj według modeli"
	],
	"RU": [
		"Реклама",
		"Очистить",
		"Копировать логи",
		"Скачать",
		"Вставьте сюда ссылки на видео",
		"Логи",
		"Вставить ссылки",
		"Настройки",
		"Качество",
		"Разрешение загружаемого видео.",
		"Тема",
		"Стиль окна программы.",
		"Сортировать по моделям"
	],
	"UK": [
		"Реклама",
		"Очистити",
		"Копіювати логи",
		"Скачати",
		"Вставте сюди посилання на відео",
		"Логи",
		"Вставити посилання",
		"Налаштування",
		"Якість",
		"Роздільна здатність завантажуваного відео.",
		"Тема",
		"Стиль вікна програми.",
		"Сортувати за моделями"
	]
}

# Текущая локализация.
CURRENT_LOCALE = LOCALES["EN"]
# Тег текущего языка.
LanguageTag = None

# Если устройство работает под управлением ОС семейства Linux.
if sys.platform in ["linux", "linux2"]:
	# Получение тега текущего языка.
	LanguageTag = locale.getlocale().split('_')[0].upper()

# Если устройство работает под управлением ОС семейства Windows.
elif sys.platform == "win32":
	# Получение сведений о системе Windows.
	WinDLL = ctypes.windll.kernel32
	WinDLL.GetUserDefaultUILanguage()
	# Получение тега текущего языка.
	LanguageTag = locale.windows_locale[WinDLL.GetUserDefaultUILanguage()].split('_')[0].upper()

# Если существует локализация, переключиться на неё.
if LanguageTag in LOCALES.keys():
    CURRENT_LOCALE = LOCALES[LanguageTag]