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
        self.green_sphere_list = arcade.SpriteList()  # Новая зеленая сфера
        self.orange_sphere_list = arcade.SpriteList()  # Новая оранжевая сфера

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

        # Состояние зеленой сферы
        self.green_sphere_active = False
        self.green_sphere_timer = 0
        self.green_sphere_spawned_this_game = False  # Была ли сфера создана в этой игре
        self.green_sphere_collected = False  # Была ли собрана сфера

        # Сообщение о переключении языка
        self.language_message = ""
        self.language_message_timer = 0

        # Сообщение о телепортации (скрытое, для отладки)
        self.teleport_message = ""
        self.teleport_message_timer = 0

        # Сообщение о режиме бессмертия
        self.god_mode_message = ""
        self.god_mode_message_timer = 0

        # Сообщение о зеленой сфере
        self.green_sphere_message = ""
        self.green_sphere_message_timer = 0

        # Сообщение об оранжевой сфере
        self.orange_sphere_message = ""
        self.orange_sphere_message_timer = 0

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
            self.god_mode_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")
            self.powerup_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
            self.freeze_sound = arcade.load_sound(":resources:sounds/ice2.wav")
            self.orange_sphere_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        except:
            self.coin_sound = None
            self.jump_sound = None
            self.hurt_sound = None
            self.teleport_sound = None
            self.god_mode_sound = None
            self.powerup_sound = None
            self.freeze_sound = None
            self.orange_sphere_sound = None

    def setup(self):
        """Настройка игры"""
        # Сброс состояний
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.green_sphere_list = arcade.SpriteList()
        self.orange_sphere_list = arcade.SpriteList()
        self.occupied_platforms.clear()

        # Зеленая сфера активна только на текущем уровне
        self.green_sphere_active = False
        self.green_sphere_timer = 0

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
            # При начале новой игры сбрасываем состояние зеленой сферы
            self.green_sphere_spawned_this_game = False
            self.green_sphere_collected = False

    def create_level(self):
        """Создание текущего уровня"""
        # Очистка
        self.platform_list.clear()
        self.coin_list.clear()
        self.enemy_list.clear()
        self.wall_list.clear()
        self.green_sphere_list.clear()
        self.orange_sphere_list.clear()
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
            platforms = [
                (100, 100, 300, 30),
                (500, 120, 200, 30),
                (200, 220, 250, 30),
                (450, 240, 180, 30),
                (300, 350, 200, 30),
                (550, 370, 150, 30),
                (400, 450, 250, 30),
            ]
        elif self.level == 6:
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
        elif self.level == 7:
            platforms = [
                (100, 80, 150, 20),
                (350, 80, 150, 20),
                (600, 80, 150, 20),
                (200, 160, 150, 20),
                (450, 160, 150, 20),
                (100, 240, 150, 20),
                (350, 240, 150, 20),
                (600, 240, 150, 20),
                (200, 320, 150, 20),
                (450, 320, 150, 20),
                (100, 400, 150, 20),
                (350, 400, 150, 20),
                (600, 400, 150, 20),
                (200, 480, 150, 20),
                (450, 480, 150, 20),
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
        elif self.level == 6:
            additional_coins = 6
        else:
            additional_coins = 8

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
        enemy_count = min(self.level + 1, 10)

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
            enemy.original_speed = ENEMY_SPEED
            enemy.frozen = False  # Новый атрибут для заморозки

            self.enemy_list.append(enemy)

        # Добавление зеленой сферы (один раз за игру)
        if not self.green_sphere_spawned_this_game and not self.green_sphere_collected:
            if random.random() < 0.3 and len(self.platform_list) > 1:
                available_platforms = [i for i in range(len(self.platform_list)) if i != self.player_start_platform]
                if available_platforms:
                    platform_idx = random.choice(available_platforms)
                    platform = self.platform_list[platform_idx]

                    green_sphere = arcade.SpriteCircle(15, GREEN_SPHERE_COLOR)
                    green_sphere.center_x = platform.center_x
                    green_sphere.center_y = platform.center_y + 50
                    self.green_sphere_list.append(green_sphere)
                    self.green_sphere_spawned_this_game = True

        # Добавление оранжевой сферы (на каждом уровне кроме первого)
        if self.level > 1 and len(self.platform_list) > 1:
            available_platforms = [i for i in range(len(self.platform_list)) if i != self.player_start_platform]
            if available_platforms:
                platform_idx = random.choice(available_platforms)
                platform = self.platform_list[platform_idx]

                orange_sphere = arcade.SpriteCircle(15, ORANGE_SPHERE_COLOR)
                orange_sphere.center_x = platform.center_x
                orange_sphere.center_y = platform.center_y + 50
                self.orange_sphere_list.append(orange_sphere)

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
            return False

        if 1 <= target_level <= MAX_LEVELS:
            old_level = self.level
            self.level = target_level
            self.setup()

            if self.teleport_sound:
                arcade.play_sound(self.teleport_sound)

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

        arcade.set_background_color(BACKGROUND_COLOR)

        self.platform_list.draw()
        self.coin_list.draw()

        # Отрисовка врагов с учетом заморозки
        for enemy in self.enemy_list:
            if hasattr(enemy, 'frozen') and enemy.frozen:
                # Рисуем замороженного врага синим цветом
                arcade.draw_circle_filled(
                    enemy.center_x,
                    enemy.center_y,
                    20,
                    FROZEN_ENEMY_COLOR
                )
                # Добавляем эффект льда (белый контур)
                arcade.draw_circle_outline(
                    enemy.center_x,
                    enemy.center_y,
                    20,
                    arcade.color.WHITE,
                    3
                )
            else:
                # Рисуем обычного врага
                arcade.draw_circle_filled(
                    enemy.center_x,
                    enemy.center_y,
                    20,
                    ENEMY_COLOR
                )

        self.green_sphere_list.draw()
        self.orange_sphere_list.draw()

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

        self.particle_system.draw()

        # Интерфейс
        arcade.draw_text(f"{loc.get('score')}: {self.score}",
                         10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"{loc.get('level')}: {self.level}/{MAX_LEVELS}",
                         10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)
        arcade.draw_text(f"{loc.get('health')}: {self.health}",
                         10, SCREEN_HEIGHT - 90, arcade.color.WHITE, 20)

        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        time_text = f"{loc.get('time')}: {minutes:02d}:{seconds:02d}"

        arcade.draw_text(time_text,
                         SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 20)

        coins_text = f"{loc.get('coins')}: {len(self.coin_list)}"
        arcade.draw_text(coins_text,
                         SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60,
                         arcade.color.WHITE, 20)

        if self.god_mode:
            arcade.draw_text(loc.get("god_mode"),
                            SCREEN_WIDTH // 2 - 80, 30,
                            arcade.color.GREEN, 24)

        # Эффект зеленой сферы
        if self.green_sphere_active:
            seconds_left = max(0, self.green_sphere_timer // 60)
            arcade.draw_text(f"Враги заморожены: {seconds_left} сек",
                            SCREEN_WIDTH // 2, 60,
                            arcade.color.CYAN, 20,
                            anchor_x="center")

        # Сообщения
        messages = []
        if self.language_message_timer > 0:
            messages.append((self.language_message, arcade.color.YELLOW, 20))
            self.language_message_timer -= 1

        if self.god_mode_message_timer > 0:
            messages.append((self.god_mode_message, arcade.color.CYAN, 20))
            self.god_mode_message_timer -= 1

        if self.green_sphere_message_timer > 0:
            messages.append((self.green_sphere_message, arcade.color.GREEN, 18))
            self.green_sphere_message_timer -= 1

        if self.orange_sphere_message_timer > 0:
            messages.append((self.orange_sphere_message, arcade.color.ORANGE, 18))
            self.orange_sphere_message_timer -= 1

        # Рисуем сообщения одно под другим
        start_y = 90 if self.green_sphere_active else 60
        for i, (text, color, size) in enumerate(messages):
            y_pos = start_y + (i * 30)
            arcade.draw_text(text,
                            SCREEN_WIDTH // 2, y_pos,
                            color, size, anchor_x="center")

        arcade.draw_text(loc.get("menu"),
                        SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90,
                        arcade.color.LIGHT_GRAY, 14)

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        self.frame_count += 1
        if self.frame_count >= 60:
            self.frame_count = 0
            self.timer_seconds += 1

        if hasattr(self, 'physics_engine') and self.physics_engine:
            self.physics_engine.update()

        # Обновление эффекта зеленой сферы
        if self.green_sphere_active:
            self.green_sphere_timer -= 1
            if self.green_sphere_timer <= 0:
                self.green_sphere_active = False
                # Восстанавливаем врагов
                for enemy in self.enemy_list:
                    enemy.frozen = False
                    enemy.speed = enemy.original_speed

        # Движение врагов (только если не заморожены)
        for enemy in self.enemy_list:
            if not (hasattr(enemy, 'frozen') and enemy.frozen):
                enemy.center_x += enemy.speed * enemy.direction

                if enemy.center_x <= enemy.left_bound:
                    enemy.center_x = enemy.left_bound
                    enemy.direction = 1
                elif enemy.center_x >= enemy.right_bound:
                    enemy.center_x = enemy.right_bound
                    enemy.direction = -1

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

        # Сбор зеленой сферы
        spheres_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.green_sphere_list
        )

        for sphere in spheres_hit:
            sphere.remove_from_sprite_lists()
            self.green_sphere_active = True
            self.green_sphere_timer = GREEN_SPHERE_DURATION
            self.green_sphere_collected = True

            # Замораживаем всех врагов
            for enemy in self.enemy_list:
                enemy.frozen = True
                enemy.speed = 0

            # Визуальный эффект
            self.particle_system.create_explosion(
                sphere.center_x,
                sphere.center_y,
                color=GREEN_SPHERE_COLOR,
                count=50
            )

            # Сообщение
            self.green_sphere_message = "Враги заморожены на 15 секунд!"
            self.green_sphere_message_timer = 90

            # Звуковой эффект
            if self.freeze_sound:
                arcade.play_sound(self.freeze_sound)

        # Сбор оранжевой сферы
        orange_spheres_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.orange_sphere_list
        )

        for sphere in orange_spheres_hit:
            sphere.remove_from_sprite_lists()

            old_score = self.score
            old_health = self.health

            self.score = max(0, self.score - ORANGE_SPHERE_SCORE_COST)
            self.health = min(100, self.health + ORANGE_SPHERE_HEALTH_RESTORE)

            self.particle_system.create_explosion(
                sphere.center_x,
                sphere.center_y,
                color=ORANGE_SPHERE_COLOR,
                count=40
            )

            score_loss = old_score - self.score
            health_gain = self.health - old_health
            self.orange_sphere_message = f"-{score_loss} очков, +{health_gain} здоровья"
            self.orange_sphere_message_timer = 90

            if self.orange_sphere_sound:
                arcade.play_sound(self.orange_sphere_sound)

        # Столкновение с врагами - ТОЛЬКО если враг не заморожен
        enemies_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        for enemy in enemies_hit:
            # Проверяем, не заморожен ли враг
            if hasattr(enemy, 'frozen') and enemy.frozen:
                continue  # Пропускаем замороженных врагов - через них можно проходить

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

        # Телепортация по уровням (F1-F7) - ТОЛЬКО В РЕЖИМЕ БЕССМЕРТИЯ
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
            elif key == arcade.key.F7:
                self.teleport_to_level(7)

        # ПЕРЕКЛЮЧЕНИЕ РЕЖИМА БЕССМЕРТИЯ (КЛАВИША M)
        if key == arcade.key.M:
            new_god_mode = not self.god_mode
            self.god_mode = new_god_mode

            if new_god_mode:
                self.particle_system.create_explosion(
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    color=(0, 255, 0),
                    count=30
                )
                self.god_mode_message = "Режим бессмертия: ВКЛЮЧЕН"
            else:
                self.particle_system.create_explosion(
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    color=(255, 0, 0),
                    count=30
                )
                self.god_mode_message = "Режим бессмертия: ВЫКЛЮЧЕН"

            self.god_mode_message_timer = 90

            if self.god_mode_sound:
                arcade.play_sound(self.god_mode_sound)
            elif self.coin_sound:
                arcade.play_sound(self.coin_sound)
            return

        # Меню и другие функции
        elif key == arcade.key.ESCAPE:
            from views import StartView
            start_view = StartView()
            self.window.show_view(start_view)
        elif key == arcade.key.LCTRL or key == arcade.key.RCTRL:
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
