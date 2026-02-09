"""
Система частиц для визуальных эффектов
"""
import arcade
import random

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def create_explosion(self, x, y, color=(255, 255, 0), count=20):
        """Создание взрыва частиц"""
        for _ in range(count):
            particle = {
                'x': x, 'y': y,
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'size': random.uniform(2, 6),
                'life': random.uniform(20, 40),
                'color': color
            }
            self.particles.append(particle)

    def create_coin_pickup(self, x, y):
        """Эффект сбора монеты"""
        self.create_explosion(x, y, (255, 215, 0), 10)

    def update(self):
        """Обновление всех частиц"""
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dy'] -= 0.1  # Гравитация
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self):
        """Отрисовка всех частиц"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 40))
            arcade.draw_circle_filled(
                particle['x'],
                particle['y'],
                particle['size'],
                (*particle['color'], alpha)
            )