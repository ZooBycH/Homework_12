import json

from .exceptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path  # путь к файлу с данными

    def load_data(self):
        """Загружает данные из файла для дальнейшего использования"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except (FileNotFoundError, json.JSONDecodeError):

            raise DataSourceBrokenException("Файл с данными поврежден")

    def save_data(self, data):
        """Перезаписывает переданные данные в файле с данными"""
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """Отдает полный список данных"""
        data = self.load_data()
        return data

    def search(self, substring):
        """Отдает посты, которые содержат substring"""

        posts = self.load_data()
        substring = substring.lower()

        matching_posts = [post for post in posts if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """Добавляет в хранилище постов определенный пост"""

        if type(post) != dict:
            raise TypeError("Dict expected for adding post")

        posts = self.load_data()
        posts.append(post)
        self.save_data(posts)
