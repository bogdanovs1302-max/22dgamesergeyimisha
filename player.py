import arcade
from constants import *


class Player(arcade.Sprite):
    """Класс игрока"""

    def __init__(self):
        # Создаем простого игрока с кружком вместо текстуры
        super().__init__()
        self.scale = 1.0
        self.speed = PLAYER_MOVE_SPEED
        self.jump_speed = PLAYER_JUMP_SPEED

        # Создаем спрайт с цветным кружком
        self.texture = arcade.make_circle_texture(20, arcade.color.BLUE)

        # Состояние игрока
        self.score = 0
        self.health = 100
        self.current_level = 1
        self.facing_right = True
        self.is_jumping = False

        # Для физического движка
        self.physics_engine = None
        self.jump_sound = None

    def setup_physics(self, physics_engine, jump_sound):
        """Настройка физического движка для игрока"""
        self.physics_engine = physics_engine
        self.jump_sound = jump_sound

    def update(self):
        """Обновление состояния игрока"""
        super().update()

    def jump(self):
        """Прыжок игрока"""
        if self.physics_engine and self.physics_engine.can_jump():
            self.change_y = self.jump_speed
            self.is_jumping = True
            if self.jump_sound:
                arcade.play_sound(self.jump_sound)