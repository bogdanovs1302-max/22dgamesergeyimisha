"""
Вспомогательные окна (стартовое и финальное)
"""
import arcade
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from data_manager import DataManager
from localization import loc

class StartView(arcade.View):
    """Начальный экран игры"""

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.top_scores = self.data_manager.get_top_scores(5)
        self.message = ""  # Сообщение для пользователя
        self.message_timer = 0

    def on_show(self):
        """Вызывается при показе окна"""
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        """Отрисовка окна"""
        self.clear()

        # Заголовок
        arcade.draw_text(loc.get("game_title"),
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                         arcade.color.GOLD, 36,
                         anchor_x="center", bold=True)

        # Инструкция
        arcade.draw_text(loc.get("press_space"),
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, 24,
                         anchor_x="center")

        # Лучшие результаты
        arcade.draw_text(loc.get("high_scores"),
                         SCREEN_WIDTH // 2, 250,
                         arcade.color.LIGHT_GRAY, 20,
                         anchor_x="center")

        if self.top_scores:
            y_pos = 210
            for i, score in enumerate(self.top_scores, 1):
                # Форматируем время
                minutes = score['time'] // 60
                seconds = score['time'] % 60
                time_str = f"{minutes:02d}:{seconds:02d}"
                
                arcade.draw_text(
                    f"{i}. {score['player']}: {score['score']} ({time_str})",
                    SCREEN_WIDTH // 2, y_pos,
                    arcade.color.LIGHT_GRAY, 16,
                    anchor_x="center"
                )
                y_pos -= 25
        else:
            arcade.draw_text(loc.get("no_scores"),
                             SCREEN_WIDTH // 2, 185,
                             arcade.color.LIGHT_GRAY, 16,
                             anchor_x="center")

        # Управление
        arcade.draw_text(loc.get("controls"),
                         10, 60,
                         arcade.color.LIGHT_GRAY, 14)

        arcade.draw_text(loc.get("delete_records"),
                         10, 40,
                         arcade.color.LIGHT_GRAY, 14)

        arcade.draw_text(loc.get("ctrl_switch"),
                         10, 20,
                         arcade.color.LIGHT_GRAY, 14)

        # Сообщение пользователю
        if self.message and self.message_timer > 0:
            arcade.draw_text(self.message,
                             SCREEN_WIDTH // 2, 100,
                             arcade.color.YELLOW, 18,
                             anchor_x="center")
            self.message_timer -= 1

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.SPACE:
            from game import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif key == arcade.key.D:
            # Удаление всех записей
            if self.data_manager.clear_scores():
                self.message = loc.get("records_deleted")
                self.message_timer = 120
                self.top_scores = []
            else:
                self.message = loc.get("delete_error")
                self.message_timer = 120

        elif key == arcade.key.LCTRL or key == arcade.key.RCTRL:
            # Переключение языка
            new_lang = loc.switch_language()
            self.message = f"{loc.get('language_switched')} ({new_lang.upper()})"
            self.message_timer = 120

class GameOverView(arcade.View):
    """Экран окончания игры"""

    def __init__(self, score, level, time_seconds):
        super().__init__()
        self.score = score
        self.level = level
        self.time_seconds = time_seconds
        self.player_name = ""
        self.data_manager = DataManager()
        
        # Язык ввода (раскладка)
        self.input_language = "en"  # По умолчанию английская
        self.language_message = ""
        self.language_message_timer = 0
        
        # Карты преобразования для русского языка (английская раскладка -> русская)
        self.russian_map = {
            # Строчные буквы (стандартная раскладка)
            'f': 'а', 'd': 'в', 'u': 'г', 'l': 'д', 't': 'е',
            ';': 'ж', 'p': 'з', 'b': 'и', 'q': 'й', 'r': 'к', 
            'k': 'л', 'v': 'м', 'y': 'н', 'j': 'о', 'g': 'п', 
            'h': 'р', 'c': 'с', 'n': 'т', 'e': 'у', 'a': 'ф',
            'w': 'ц', 'x': 'ч', 'i': 'ш', 'o': 'щ',
            's': 'ы', 'm': 'ь', "'": 'э',
            'z': 'я',
            
            # Заглавные буквы
            'F': 'А', 'D': 'В', 'U': 'Г', 'L': 'Д', 'T': 'Е',
            'P': 'З', 'B': 'И', 'Q': 'Й', 'R': 'К',
            'K': 'Л', 'V': 'М', 'Y': 'Н', 'J': 'О', 'G': 'П',
            'H': 'Р', 'C': 'С', 'N': 'Т', 'E': 'У', 'A': 'Ф',
            'W': 'Ц', 'X': 'Ч', 'I': 'Ш', 'O': 'Щ',
            'S': 'Ы', 'M': 'Ь',
            'Z': 'Я',
            
            # Буква Б и запятая
            ',': 'б', '<': 'Б',
            # Точка и буква Ю
            '.': 'ю', '>': 'Ю',
        }

    def on_show(self):
        """Вызывается при показе окна"""
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        """Отрисовка окна"""
        self.clear()

        # Заголовок
        arcade.draw_text(loc.get("game_over"),
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                         arcade.color.WHITE, 48,
                         anchor_x="center")

        # Результат
        arcade.draw_text(f"{loc.get('score')}: {self.score}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                         arcade.color.GOLD, 36,
                         anchor_x="center")

        # Уровень
        arcade.draw_text(f"{loc.get('level')}: {self.level}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.SILVER, 28,
                         anchor_x="center")
        
        # Время
        minutes = self.time_seconds // 60
        seconds = self.time_seconds % 60
        arcade.draw_text(f"{loc.get('total_time')}: {minutes:02d}:{seconds:02d}",
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                         arcade.color.CYAN, 24,
                         anchor_x="center")

        # Инструкция
        arcade.draw_text(loc.get("enter_name"),
                         SCREEN_WIDTH // 2, 200,
                         arcade.color.LIGHT_GRAY, 20,
                         anchor_x="center")

        # Имя игрока с курсором
        arcade.draw_text(f"{loc.get('name')}: {self.player_name}_",
                         SCREEN_WIDTH // 2, 150,
                         arcade.color.WHITE, 24,
                         anchor_x="center")
        
        # Индикатор языка ввода
        lang_text = "РУС" if self.input_language == "ru" else "ENG"
        lang_color = arcade.color.RED if self.input_language == "ru" else arcade.color.BLUE
        arcade.draw_text(f"{loc.get('input_language')}: {lang_text}",
                         SCREEN_WIDTH // 2, 120,
                         lang_color, 18,
                         anchor_x="center")
        
        # Подсказка по переключению языка
        arcade.draw_text(loc.get("switch_input_language"),
                         SCREEN_WIDTH // 2, 95,
                         arcade.color.LIGHT_YELLOW, 14,
                         anchor_x="center")
        
        # Подсказка по раскладке (только для русского)
        if self.input_language == "ru":
            arcade.draw_text(loc.get("use_english_for_russian"),
                             SCREEN_WIDTH // 2, 75,
                             arcade.color.LIGHT_YELLOW, 12,
                             anchor_x="center")
            arcade.draw_text("f=а, d=в, u=г, l=д, t=е, ,=б, .=ю",
                             SCREEN_WIDTH // 2, 60,
                             arcade.color.LIGHT_YELLOW, 10,
                             anchor_x="center")

        # Сообщение о смене языка
        if self.language_message_timer > 0:
            arcade.draw_text(self.language_message,
                             SCREEN_WIDTH // 2, 180,
                             arcade.color.YELLOW, 16,
                             anchor_x="center")
            self.language_message_timer -= 1

        arcade.draw_text(loc.get("back_to_menu"),
                         10, 30,
                         arcade.color.LIGHT_GRAY, 14)

    def on_key_press(self, key, modifiers):
        """Обработка ввода имени с переключением языка по Alt"""
        # Enter для сохранения
        if key == arcade.key.ENTER and self.player_name.strip():
            # Сохраняем результат с временем
            self.data_manager.save_score(
                self.player_name.strip(), 
                self.score, 
                self.level, 
                self.time_seconds
            )

            # Возвращаемся в главное меню
            start_view = StartView()
            self.window.show_view(start_view)

        # Backspace для удаления
        elif key == arcade.key.BACKSPACE and self.player_name:
            self.player_name = self.player_name[:-1]

        # Escape для выхода без сохранения
        elif key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)

        # Ctrl для переключения языка интерфейса
        elif key == arcade.key.LCTRL or key == arcade.key.RCTRL:
            new_lang = loc.switch_language()
            self.language_message = f"{loc.get('interface_language')}: {new_lang.upper()}"
            self.language_message_timer = 90

        # Alt для переключения языка ввода (раскладки)
        elif key == arcade.key.LALT or key == arcade.key.RALT:
            self.input_language = "ru" if self.input_language == "en" else "en"
            lang_name = "Русский" if self.input_language == "ru" else "English"
            self.language_message = f"{loc.get('input_language')}: {lang_name}"
            self.language_message_timer = 90

        # Пробел
        elif key == arcade.key.SPACE and len(self.player_name) < 20:
            self.player_name += " "

        # Обработка букв в зависимости от выбранного языка
        elif len(self.player_name) < 20:
            if self.input_language == "en":
                # АНГЛИЙСКИЙ ЯЗЫК - прямой ввод
                if key == arcade.key.A:
                    self.player_name += 'A' if modifiers & arcade.key.MOD_SHIFT else 'a'
                elif key == arcade.key.B:
                    self.player_name += 'B' if modifiers & arcade.key.MOD_SHIFT else 'b'
                elif key == arcade.key.C:
                    self.player_name += 'C' if modifiers & arcade.key.MOD_SHIFT else 'c'
                elif key == arcade.key.D:
                    self.player_name += 'D' if modifiers & arcade.key.MOD_SHIFT else 'd'
                elif key == arcade.key.E:
                    self.player_name += 'E' if modifiers & arcade.key.MOD_SHIFT else 'e'
                elif key == arcade.key.F:
                    self.player_name += 'F' if modifiers & arcade.key.MOD_SHIFT else 'f'
                elif key == arcade.key.G:
                    self.player_name += 'G' if modifiers & arcade.key.MOD_SHIFT else 'g'
                elif key == arcade.key.H:
                    self.player_name += 'H' if modifiers & arcade.key.MOD_SHIFT else 'h'
                elif key == arcade.key.I:
                    self.player_name += 'I' if modifiers & arcade.key.MOD_SHIFT else 'i'
                elif key == arcade.key.J:
                    self.player_name += 'J' if modifiers & arcade.key.MOD_SHIFT else 'j'
                elif key == arcade.key.K:
                    self.player_name += 'K' if modifiers & arcade.key.MOD_SHIFT else 'k'
                elif key == arcade.key.L:
                    self.player_name += 'L' if modifiers & arcade.key.MOD_SHIFT else 'l'
                elif key == arcade.key.M:
                    self.player_name += 'M' if modifiers & arcade.key.MOD_SHIFT else 'm'
                elif key == arcade.key.N:
                    self.player_name += 'N' if modifiers & arcade.key.MOD_SHIFT else 'n'
                elif key == arcade.key.O:
                    self.player_name += 'O' if modifiers & arcade.key.MOD_SHIFT else 'o'
                elif key == arcade.key.P:
                    self.player_name += 'P' if modifiers & arcade.key.MOD_SHIFT else 'p'
                elif key == arcade.key.Q:
                    self.player_name += 'Q' if modifiers & arcade.key.MOD_SHIFT else 'q'
                elif key == arcade.key.R:
                    self.player_name += 'R' if modifiers & arcade.key.MOD_SHIFT else 'r'
                elif key == arcade.key.S:
                    self.player_name += 'S' if modifiers & arcade.key.MOD_SHIFT else 's'
                elif key == arcade.key.T:
                    self.player_name += 'T' if modifiers & arcade.key.MOD_SHIFT else 't'
                elif key == arcade.key.U:
                    self.player_name += 'U' if modifiers & arcade.key.MOD_SHIFT else 'u'
                elif key == arcade.key.V:
                    self.player_name += 'V' if modifiers & arcade.key.MOD_SHIFT else 'v'
                elif key == arcade.key.W:
                    self.player_name += 'W' if modifiers & arcade.key.MOD_SHIFT else 'w'
                elif key == arcade.key.X:
                    self.player_name += 'X' if modifiers & arcade.key.MOD_SHIFT else 'x'
                elif key == arcade.key.Y:
                    self.player_name += 'Y' if modifiers & arcade.key.MOD_SHIFT else 'y'
                elif key == arcade.key.Z:
                    self.player_name += 'Z' if modifiers & arcade.key.MOD_SHIFT else 'z'
                    
                elif 48 <= key <= 57:  # 0-9
                    self.player_name += chr(key)
                    
                elif key == arcade.key.PERIOD:
                    self.player_name += '.'
                elif key == arcade.key.COMMA:
                    self.player_name += ','
                    
            else:
                # РУССКИЙ ЯЗЫК - преобразование через английскую раскладку
                char = None
                
                # Буквы
                if key == arcade.key.A:
                    char = 'A' if modifiers & arcade.key.MOD_SHIFT else 'a'
                elif key == arcade.key.B:
                    char = 'B' if modifiers & arcade.key.MOD_SHIFT else 'b'
                elif key == arcade.key.C:
                    char = 'C' if modifiers & arcade.key.MOD_SHIFT else 'c'
                elif key == arcade.key.D:
                    char = 'D' if modifiers & arcade.key.MOD_SHIFT else 'd'
                elif key == arcade.key.E:
                    char = 'E' if modifiers & arcade.key.MOD_SHIFT else 'e'
                elif key == arcade.key.F:
                    char = 'F' if modifiers & arcade.key.MOD_SHIFT else 'f'
                elif key == arcade.key.G:
                    char = 'G' if modifiers & arcade.key.MOD_SHIFT else 'g'
                elif key == arcade.key.H:
                    char = 'H' if modifiers & arcade.key.MOD_SHIFT else 'h'
                elif key == arcade.key.I:
                    char = 'I' if modifiers & arcade.key.MOD_SHIFT else 'i'
                elif key == arcade.key.J:
                    char = 'J' if modifiers & arcade.key.MOD_SHIFT else 'j'
                elif key == arcade.key.K:
                    char = 'K' if modifiers & arcade.key.MOD_SHIFT else 'k'
                elif key == arcade.key.L:
                    char = 'L' if modifiers & arcade.key.MOD_SHIFT else 'l'
                elif key == arcade.key.M:
                    char = 'M' if modifiers & arcade.key.MOD_SHIFT else 'm'
                elif key == arcade.key.N:
                    char = 'N' if modifiers & arcade.key.MOD_SHIFT else 'n'
                elif key == arcade.key.O:
                    char = 'O' if modifiers & arcade.key.MOD_SHIFT else 'o'
                elif key == arcade.key.P:
                    char = 'P' if modifiers & arcade.key.MOD_SHIFT else 'p'
                elif key == arcade.key.Q:
                    char = 'Q' if modifiers & arcade.key.MOD_SHIFT else 'q'
                elif key == arcade.key.R:
                    char = 'R' if modifiers & arcade.key.MOD_SHIFT else 'r'
                elif key == arcade.key.S:
                    char = 'S' if modifiers & arcade.key.MOD_SHIFT else 's'
                elif key == arcade.key.T:
                    char = 'T' if modifiers & arcade.key.MOD_SHIFT else 't'
                elif key == arcade.key.U:
                    char = 'U' if modifiers & arcade.key.MOD_SHIFT else 'u'
                elif key == arcade.key.V:
                    char = 'V' if modifiers & arcade.key.MOD_SHIFT else 'v'
                elif key == arcade.key.W:
                    char = 'W' if modifiers & arcade.key.MOD_SHIFT else 'w'
                elif key == arcade.key.X:
                    char = 'X' if modifiers & arcade.key.MOD_SHIFT else 'x'
                elif key == arcade.key.Y:
                    char = 'Y' if modifiers & arcade.key.MOD_SHIFT else 'y'
                elif key == arcade.key.Z:
                    char = 'Z' if modifiers & arcade.key.MOD_SHIFT else 'z'
                
                # Цифры
                elif 48 <= key <= 57:  # 0-9
                    self.player_name += chr(key)  # Цифры остаются цифрами
                    
                # Точка и запятая
                elif key == arcade.key.COMMA:
                    char = '<' if modifiers & arcade.key.MOD_SHIFT else ','
                elif key == arcade.key.PERIOD:
                    char = '>' if modifiers & arcade.key.MOD_SHIFT else '.'
                
                # Преобразуем символ в русскую букву, если есть в карте
                if char and char in self.russian_map:
                    self.player_name += self.russian_map[char]
