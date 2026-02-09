"""
Система локализации для переключения языка
"""


class Localization:
    def __init__(self):
        self.current_language = "ru"  # По умолчанию русский
        self.texts = {
            "ru": {
                # Стартовое меню
                "game_title": "Coin Collector Adventure",
                "press_space": "Нажмите SPACE для начала игры",
                "high_scores": "Лучшие результаты:",
                "no_scores": "Нет сохраненных результатов",
                "controls": "Управление: ← → движение, SPACE прыжок",
                "delete_records": "D - удалить все записи",
                "ctrl_switch": "Ctrl - переключить язык интерфейса",

                # Игровой интерфейс
                "score": "Счет",
                "level": "Уровень",
                "health": "Здоровье",
                "time": "Время",
                "coins": "Монеты",
                "god_mode": "БЕССМЕРТИЕ",
                "menu": "ESC - меню",

                # Экран окончания
                "game_over": "Игра Окончена!",
                "enter_name": "Введите имя и нажмите ENTER для сохранения",
                "name": "Имя",
                "back_to_menu": "ESC - выйти в меню",
                "total_time": "Общее время",
                "input_language": "Язык ввода",
                "interface_language": "Язык интерфейса",
                "switch_input_language": "Alt - переключить язык ввода",
                "use_english_for_russian": "Используйте английскую раскладку для русских букв",
                "keyboard_layout_hint": "f=а, d=в, u=г, l=д, t=е, Shift для заглавных",

                # Сообщения
                "records_deleted": "Все записи удалены!",
                "delete_error": "Ошибка при удалении записей",
                "language_switched": "Язык переключен",
            },
            "en": {
                # Стартовое меню
                "game_title": "Coin Collector Adventure",
                "press_space": "Press SPACE to start the game",
                "high_scores": "High Scores:",
                "no_scores": "No saved scores",
                "controls": "Controls: ← → move, SPACE jump",
                "delete_records": "D - delete all records",
                "ctrl_switch": "Ctrl - switch interface language",

                # Игровой интерфейс
                "score": "Score",
                "level": "Level",
                "health": "Health",
                "time": "Time",
                "coins": "Coins",
                "god_mode": "GOD MODE",
                "menu": "ESC - menu",

                # Экран окончания
                "game_over": "Game Over!",
                "enter_name": "Enter name and press ENTER to save",
                "name": "Name",
                "back_to_menu": "ESC - back to menu",
                "total_time": "Total time",
                "input_language": "Input language",
                "interface_language": "Interface language",
                "switch_input_language": "Alt - switch input language",
                "use_english_for_russian": "Use English layout for Russian letters",
                "keyboard_layout_hint": "f=а, d=в, u=г, l=д, t=е, Shift for uppercase",

                # Сообщения
                "records_deleted": "All records deleted!",
                "delete_error": "Error deleting records",
                "language_switched": "Language switched",
            }
        }

    def get(self, key):
        """Получение текста на текущем языке"""
        if self.current_language in self.texts and key in self.texts[self.current_language]:
            return self.texts[self.current_language][key]
        return key

    def switch_language(self):
        """Переключение языка интерфейса"""
        if self.current_language == "ru":
            self.current_language = "en"
            return "en"
        else:
            self.current_language = "ru"
            return "ru"


# Глобальный экземпляр локализации
loc = Localization()