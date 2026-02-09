"""
Менеджер данных для сохранения результатов в CSV
"""
import csv
import os
from datetime import datetime
from pathlib import Path

class DataManager:
    def __init__(self, filename="high_scores.csv"):
        self.filename = filename
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.filepath = self.data_dir / filename

        if not self.filepath.exists():
            self.create_default_file()
        else:
            # Проверяем, есть ли колонка Time в существующем файле
            self.check_and_update_file_format()

    def check_and_update_file_format(self):
        """Проверяет формат файла и обновляет при необходимости"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                
                if headers is None or 'Time' not in headers:
                    # Старый формат, нужно обновить
                    self.convert_old_format()
        except Exception:
            # Если ошибка чтения, создаем новый файл
            self.create_default_file()

    def convert_old_format(self):
        """Конвертирует старый формат файла в новый"""
        old_scores = []
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    old_scores.append({
                        'player': row.get('Player', ''),
                        'score': int(row.get('Score', 0)),
                        'level': int(row.get('Level', 1)),
                        'date': row.get('Date', '')
                    })
        except:
            pass
            
        # Создаем новый файл с обновленным форматом
        self.create_default_file()
        
        # Сохраняем старые результаты с временем по умолчанию (99999)
        for score in old_scores:
            self.save_score(score['player'], score['score'], score['level'], 99999)

    def create_default_file(self):
        """Создание файла с заголовками"""
        with open(self.filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Player", "Score", "Level", "Time", "Date"])

    def save_score(self, player_name, score, level, time_seconds):
        """Сохранение результата игрока с временем"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, score, level, time_seconds, date])

    def get_top_scores(self, limit=10):
        """Получение лучших результатов - сначала по очкам, потом по времени"""
        scores = []

        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Обрабатываем старый и новый форматы
                        player = row.get('Player', '')
                        score = int(row.get('Score', 0))
                        level = int(row.get('Level', 1))
                        
                        # Время может отсутствовать в старых записях
                        if 'Time' in row and row['Time']:
                            time_val = int(row['Time'])
                        else:
                            time_val = 99999  # Большое значение для старых записей
                            
                        date = row.get('Date', '')
                        
                        scores.append({
                            'player': player,
                            'score': score,
                            'level': level,
                            'time': time_val,
                            'date': date
                        })
                    except (ValueError, KeyError):
                        continue

        # Сортировка: сначала по очкам (больше = лучше), потом по времени (меньше = лучше)
        scores.sort(key=lambda x: (-x['score'], x['time']))
        return scores[:limit]

    def clear_scores(self):
        """Удаление всех записей"""
        try:
            if self.filepath.exists():
                self.filepath.unlink()
                self.create_default_file()
                return True
        except Exception:
            pass
        return False