"""
Основной игровой класс
"""
import arcade
import random
import os
from constants import *
from particle_system import ParticleSystem
from localization import loc

class GameView(arcade.View):
    """Основное игровое окно"""

    def __init__(self):
        super().__init__()

        # Списки спрайтов
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Игрок и его состояние
        self.player_sprite = None
        self.score = 0
        self.level = 1
        self.health = 100

        # Секундомер
        self.timer_seconds = 0  # Секунды
        self.frame_count = 0  # Счетчик кадров

        # Режим бессмертия
        self.god_mode = False

        # Сообщение о переключении языка
        self.language_message = ""
        self.language_message_timer = 0

        # Сообщение о телепортации (скрытое, для отладки)
        self.teleport_message = ""
        self.teleport_message_timer = 0

        # Система частиц
        self.particle_system = ParticleSystem()

        # Звуки
        self.setup_sounds()

        # Для отслеживания занятых платформ
        self.occupied_platforms = set()
        self.player_start_platform = 0

    def setup_sounds(self):
        """Настройка звуков игры"""
        try:
            self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
            self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
            self.hurt_sound = arcade.load_sound(":resources:sounds/hurt2.wav")
            self.teleport_sound = arcade.load_sound(":resources:sounds/upgrade4.wav")
        except:
            self.coin_sound = None
            self.jump_sound = None
            self.hurt_sound = None
            self.teleport_sound = None

    def setup(self):
        """Настройка игры"""
        # Сброс состояний
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.occupied_platforms.clear()

        # Создание игрока
        self.player_sprite = arcade.SpriteCircle(20, PLAYER_COLOR)
        self.player_list.append(self.player_sprite)

        # Создание уровня
        self.create_level()

        # Размещаем игрока на стартовой платформе
        if self.platform_list:
            start_platform = self.platform_list[self.player_start_platform]
            self.player_sprite.center_x = start_platform.center_x
            self.player_sprite.center_y = start_platform.center_y + 40

        # Настройка физического движка
        all_walls = arcade.SpriteList()
        all_walls.extend(self.platform_list)
        all_walls.extend(self.wall_list)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            all_walls,
            gravity_constant=GRAVITY
        )

        # Сброс счета для первого уровня
        if self.level == 1:
            self.score = 0
            self.health = 100
            self.timer_seconds = 0
            self.frame_count = 0

    def create_level(self):
        """Создание текущего уровня"""
        # Очистка
        self.platform_list.clear()
        self.coin_list.clear()
        self.enemy_list.clear()
        self.wall_list.clear()
        self.occupied_platforms.clear()

        # Создание платформ
        platforms = []
        self.player_start_platform = 0

        if self.level == 1:
            platforms = [
                (0, 100, 500, 30),
                (550, 200, 200, 30),
                (300, 300, 200, 30),
                (100, 400, 200, 30),
                (450, 450, 200, 30),
            ]
        elif self.level == 2:
            platforms = [
                (50, 100, 200, 30),
                (350, 150, 200, 30),
                (100, 220, 200, 30),
                (450, 290, 200, 30),
                (200, 360, 200, 30),
                (550, 430, 200, 30),
            ]
        elif self.level == 3:
            platforms = [
                (100, 100, 200, 30),
                (400, 150, 200, 30),
                (100, 220, 200, 30),
                (400, 290, 200, 30),
                (100, 360, 200, 30),
                (400, 430, 200, 30),
                (100, 500, 200, 30),
            ]
        elif self.level == 4:
            platforms = [
                (50, 100, 180, 25),
                (300, 140, 180, 25),
                (550, 180, 180, 25),
                (150, 240, 180, 25),
                (400, 280, 180, 25),
                (650, 320, 180, 25),
                (250, 380, 180, 25),
                (500, 420, 180, 25),
            ]
        elif self.level == 5:
            # Уровень 5
            platforms = [
                (100, 100, 300, 30),
                (500, 120, 200, 30),
                (200, 220, 250, 30),
                (450, 240, 180, 30),
                (300, 350, 200, 30),
                (550, 370, 150, 30),
                (400, 450, 250, 30),
            ]
        else:
            platforms = [
                (50, 80, 140, 20),
                (250, 120, 140, 20),
                (450, 160, 140, 20),
                (650, 200, 140, 20),
                (150, 240, 140, 20),
                (350, 280, 140, 20),
                (550, 320, 140, 20),
                (100, 360, 140, 20),
                (300, 400, 140, 20),
                (500, 440, 140, 20),
                (200, 480, 140, 20),
            ]

        # Добавление платформ
        for x, y, width, height in platforms:
            platform = arcade.SpriteSolidColor(width, height, PLATFORM_COLOR)
            platform.center_x = x + width / 2
            platform.center_y = y + height / 2
            self.platform_list.append(platform)

        # Добавление границ
        self.create_walls()

        # ГАРАНТИРОВАННЫЕ МОНЕТЫ НА КАЖДОЙ ПЛАТФОРМЕ (кроме стартовой)
        for i, platform in enumerate(self.platform_list):
            if i == self.player_start_platform:
                continue

            # Добавляем минимум 1 монету на каждую платформу
            coin = arcade.SpriteCircle(10, COIN_COLOR)
            coin.center_x = platform.center_x
            coin.center_y = platform.center_y + 40
            self.coin_list.append(coin)

        # Добавление дополнительных монет
        if self.level == 1:
            additional_coins = 4
        elif self.level == 2:
            additional_coins = 4
        elif self.level == 3:
            additional_coins = 5
        elif self.level == 4:
            additional_coins = 5
        elif self.level == 5:
            additional_coins = 5
        else:
            additional_coins = 6

        # Добавляем дополнительные монеты
        for i in range(additional_coins):
            if self.platform_list:
                platform_idx = random.randint(0, len(self.platform_list) - 1)
                platform = self.platform_list[platform_idx]

                coin = arcade.SpriteCircle(10, COIN_COLOR)
                coin.center_x = platform.center_x + random.randint(-60, 60)
                coin.center_y = platform.center_y + 40

                if coin.center_x < platform.left + 15:
                    coin.center_x = platform.left + 15
                if coin.center_x > platform.right - 15:
                    coin.center_x = platform.right - 15

                self.coin_list.append(coin)

        # Добавление врагов
        enemy_count = min(self.level + 1, 8)

        # Список доступных платформ (исключая стартовую)
        available_platform_indices = list(range(len(self.platform_list)))
        if self.player_start_platform in available_platform_indices:
            available_platform_indices.remove(self.player_start_platform)

        for i in range(enemy_count):
            if not available_platform_indices:
                break

            platform_idx = random.choice(available_platform_indices)
            available_platform_indices.remove(platform_idx)
            platform = self.platform_list[platform_idx]

            enemy = arcade.SpriteCircle(20, ENEMY_COLOR)
            enemy.center_x = platform.center_x
            enemy.center_y = platform.center_y + 40
            enemy.direction = 1 if random.random() > 0.5 else -1
            enemy.speed = ENEMY_SPEED
            enemy.left_bound = platform.left + 30
            enemy.right_bound = platform.right - 30

            self.enemy_list.append(enemy)

    def create_walls(self):
        """Создание невидимых границ"""
        left_wall = arcade.SpriteSolidColor(50, SCREEN_HEIGHT * 3, (0, 0, 0, 0))
        left_wall.center_x = -25
        left_wall.center_y = SCREEN_HEIGHT // 2
        self.wall_list.append(left_wall)

        right_wall = arcade.SpriteSolidColor(50, SCREEN_HEIGHT * 3, (0, 0, 0, 0))
        right_wall.center_x = SCREEN_WIDTH + 25
        right_wall.center_y = SCREEN_HEIGHT // 2
        self.wall_list.append(right_wall)

    def teleport_to_level(self, target_level):
        """Телепортация на указанный уровень (только в режиме бессмертия)"""
        if not self.god_mode:
            # Только в режиме бессмертия!
            return False
            
        if 1 <= target_level <= MAX_LEVELS:
            old_level = self.level
            self.level = target_level
            self.setup()
            
            # Скрытое сообщение (можно включить для отладки)
            # self.teleport_message = f"Телепортация: уровень {old_level} → {target_level}"
            # self.teleport_message_timer = 60
            
            # Звук телепортации
            if self.teleport_sound:
                arcade.play_sound(self.teleport_sound)
                
            # Визуальный эффект
            self.particle_system.create_explosion(
                self.player_sprite.center_x,
                self.player_sprite.center_y,
                color=(100, 100, 255),
                count=30
            )
            return True
        return False

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Фон
        arcade.set_background_color(BACKGROUND_COLOR)

        # Игровые объекты
        self.platform_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()

        # Игрок (зеленый в режиме бессмертия)
        if self.god_mode:
            arcade.draw_circle_filled(
                self.player_sprite.center_x,
                self.player_sprite.center_y,
                20,
                (0, 255, 0)
            )
        else:
            arcade.draw_circle_filled(
                self.player_sprite.center_x,
                self.player_sprite.center_y,
                20,
                PLAYER_COLOR
            )

        # Частицы
        self.particle_system.draw()

        # Интерфейс - левая колонка
        arcade.draw_text(f"{loc.get('score')}: {self.score}", 
                         10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"{loc.get('level')}: {self.level}/{MAX_LEVELS}", 
                         10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)
        arcade.draw_text(f"{loc.get('health')}: {self.health}", 
                         10, SCREEN_HEIGHT - 90, arcade.color.WHITE, 20)

        # Интерфейс - правая колонка (секундомер)
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        time_text = f"{loc.get('time')}: {minutes:02d}:{seconds:02d}"
        
        arcade.draw_text(time_text, 
                         SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30, 
                         arcade.color.WHITE, 20)
        
        # Монеты
        coins_text = f"{loc.get('coins')}: {len(self.coin_list)}"
        arcade.draw_text(coins_text, 
                         SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60, 
                         arcade.color.WHITE, 20)

        # Режим бессмертия
        if self.god_mode:
            arcade.draw_text(loc.get("god_mode"), 
                            SCREEN_WIDTH // 2 - 80, 30, 
                            arcade.color.GREEN, 24)

        # Сообщение о переключении языка
        if self.language_message_timer > 0:
            arcade.draw_text(self.language_message, 
                            SCREEN_WIDTH // 2, 80, 
                            arcade.color.YELLOW, 20, anchor_x="center")
            self.language_message_timer -= 1
            
        # Сообщение о телепортации (СКРЫТО)
        # if self.teleport_message_timer > 0:
        #     arcade.draw_text(self.teleport_message, 
        #                     SCREEN_WIDTH // 2, 110, 
        #                     arcade.color.CYAN, 20, anchor_x="center")
        #     self.teleport_message_timer -= 1

        # Управление (без упоминания телепортации)
        arcade.draw_text(loc.get("menu"), 
                        SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90, 
                        arcade.color.LIGHT_GRAY, 14)

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        # Обновление секундомера
        self.frame_count += 1
        if self.frame_count >= 60:  # 60 FPS = 1 секунда
            self.frame_count = 0
            self.timer_seconds += 1

        # Физика
        if hasattr(self, 'physics_engine') and self.physics_engine:
            self.physics_engine.update()

        # Движение врагов
        for enemy in self.enemy_list:
            enemy.center_x += enemy.speed * enemy.direction

            if enemy.center_x <= enemy.left_bound:
                enemy.center_x = enemy.left_bound
                enemy.direction = 1
            elif enemy.center_x >= enemy.right_bound:
                enemy.center_x = enemy.right_bound
                enemy.direction = -1

        # Частицы
        self.particle_system.update()

        # Сбор монет
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10

            if self.coin_sound:
                arcade.play_sound(self.coin_sound)

            self.particle_system.create_coin_pickup(
                coin.center_x, coin.center_y
            )

        # Столкновение с врагами
        enemies_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        for enemy in enemies_hit:
            if not self.god_mode:
                self.health -= 5

                if self.health <= 0:
                    self.game_over()
                    return

                if self.hurt_sound:
                    arcade.play_sound(self.hurt_sound)

            # Слабое отталкивание
            if enemy.center_x > self.player_sprite.center_x:
                self.player_sprite.center_x -= 15
            else:
                self.player_sprite.center_x += 15

        # Завершение уровня
        if len(self.coin_list) == 0:
            self.level += 1
            if self.level <= MAX_LEVELS:
                self.setup()
            else:
                self.game_over()

        # Падение
        if self.player_sprite.center_y < -100:
            if not self.god_mode:
                self.game_over()
            else:
                if self.platform_list:
                    start_platform = self.platform_list[self.player_start_platform]
                    self.player_sprite.center_x = start_platform.center_x
                    self.player_sprite.center_y = start_platform.center_y + 40
                    self.player_sprite.change_x = 0
                    self.player_sprite.change_y = 0

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        # Движение
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVE_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVE_SPEED
        elif key == arcade.key.SPACE or key == arcade.key.W or key == arcade.key.UP:
            if hasattr(self, 'physics_engine') and self.physics_engine and self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                if self.jump_sound:
                    arcade.play_sound(self.jump_sound)
        
        # Телепортация по уровням (F1-F6) - ТОЛЬКО В РЕЖИМЕ БЕССМЕРТИЯ
        if self.god_mode:
            if key == arcade.key.F1:
                self.teleport_to_level(1)
            elif key == arcade.key.F2:
                self.teleport_to_level(2)
            elif key == arcade.key.F3:
                self.teleport_to_level(3)
            elif key == arcade.key.F4:
                self.teleport_to_level(4)
            elif key == arcade.key.F5:
                self.teleport_to_level(5)
            elif key == arcade.key.F6:
                self.teleport_to_level(6)
            
        # Меню и другие функции
        elif key == arcade.key.ESCAPE:
            from views import StartView
            start_view = StartView()
            self.window.show_view(start_view)
        elif key == arcade.key.M:
            # Режим бессмертия
            self.god_mode = not self.god_mode
            if self.coin_sound:
                arcade.play_sound(self.coin_sound)
        elif key == arcade.key.LCTRL or key == arcade.key.RCTRL:
            # Переключение языка интерфейса
            new_lang = loc.switch_language()
            self.language_message = f"{loc.get('language_switched')} ({new_lang.upper()})"
            self.language_message_timer = 120

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.LEFT, arcade.key.RIGHT,
                   arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0

    def game_over(self):
        """Завершение игры"""
        from views import GameOverView
        game_over_view = GameOverView(self.score, self.level, self.timer_seconds)
        self.window.show_view(game_over_view)