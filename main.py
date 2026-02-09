"""
Главный файл игры - точка входа
"""
import arcade
import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views import StartView

import warnings
warnings.filterwarnings("ignore", message="draw_text is an extremely slow function")

def main():
    """Главная функция запуска игры"""
    # Проверяем наличие необходимых модулей
    try:
        import arcade
        print("Arcade загружен успешно")
    except ImportError:
        print("Ошибка: Установите библиотеку arcade: pip install arcade")
        return
    
    # Создаем окно
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # Настраиваем окно
    window.set_update_rate(1/60)  # 60 FPS
    
    # Показываем стартовый экран
    start_view = StartView()
    window.show_view(start_view)
    
    # Запускаем игру
    arcade.run()

# Точка входа в программу
if __name__ == "__main__":
    main()