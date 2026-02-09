# texture_manager.py (упрощенная версия)
import arcade

class TextureManager:
    def __init__(self):
        self.textures = {}
        self.create_simple_textures()
    
    def create_simple_textures(self):
        """Создание простых текстур"""
        try:
            # Используем правильные размеры
            self.textures['player'] = arcade.make_circle_texture(40, (65, 105, 225))  # 40px
            self.textures['enemy'] = arcade.make_circle_texture(40, (220, 20, 60))    # 40px  
            self.textures['coin'] = arcade.make_circle_texture(20, (255, 215, 0))     # 20px
            
            # Платформа
            self.textures['platform'] = arcade.make_soft_square_texture(
                100, (101, 67, 33), outer_alpha=255  # 100px
            )
            
            print("Текстуры успешно созданы")
            
        except Exception as e:
            print(f"Ошибка при создании текстур: {e}")
            # Если не получилось, используем None
            self.textures = {}
    
    def get_texture(self, name):
        """Получение текстуры по имени"""
        return self.textures.get(name)

# Глобальный экземпляр
texture_manager = TextureManager()