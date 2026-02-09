import arcade
import random
from constants import *


class Enemy(arcade.Sprite):
    """Класс врага с улучшенным ИИ и защитой от падения"""

    def __init__(self, x, y, platform_left=None, platform_right=None):
        super().__init__()
        self.width = 40
        self.height = 40
        self.center_x = x
        self.center_y = y
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1 - вправо, -1 - влево
        self.move_timer = 0
        self.color = ENEMY_COLOR
        
        # Границы для патрулирования (если указаны)
        self.platform_left = platform_left
        self.platform_right = platform_right
        self.has_bounds = platform_left is not None and platform_right is not None
        
        # Время до смены направления
        self.change_direction_time = random.randint(60, 120)
        
        # Физические свойства
        self.change_y = 0
        self.on_ground = False

    def draw(self):
        """Отрисовка врага с глазами, показывающими направление"""
        # Тело
        arcade.draw_rectangle_filled(
            self.center_x, self.center_y,
            self.width, self.height,
            self.color
        )
        
        # Глаза
        eye_offset = 10 if self.direction == 1 else -10
        arcade.draw_circle_filled(
            self.center_x + eye_offset, self.center_y + 5,
            6, arcade.color.WHITE
        )
        arcade.draw_circle_filled(
            self.center_x + eye_offset, self.center_y + 5,
            3, arcade.color.BLACK
        )

    def update(self):
        """Обновление врага с интеллектуальным патрулированием"""
        # Случайная смена направления через время
        self.move_timer += 1
        if self.move_timer > self.change_direction_time:
            self.direction *= -1
            self.move_timer = 0
            self.change_direction_time = random.randint(60, 120)
        
        # Ограничение движения в пределах платформы
        if self.has_bounds:
            new_x = self.center_x + (self.speed * self.direction)
            
            # Если враг достиг края платформы - развернуться
            if new_x < self.platform_left + 20:
                self.direction = 1
                new_x = self.platform_left + 20
            elif new_x > self.platform_right - 20:
                self.direction = -1
                new_x = self.platform_right - 20
                
            self.center_x = new_x
        else:
            # Свободное движение (для тестовых уровней)
            self.center_x += self.speed * self.direction
        
        # Гравитация
        self.center_y -= GRAVITY
        
        # Защита от падения в бездну
        if self.center_y < -50:
            self.remove_from_sprite_lists()