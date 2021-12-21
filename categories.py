"""Работа с категориями расходов"""
from typing import Dict, List, NamedTuple

import db

class Category(NamedTuple):
    """Структура категории"""
    name: str
    codename: str
    is_regular_expense: bool


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий расходов из БД"""
        categories = db.fetchall(
            "category", "name codename is_regular_expense".split()
        )
        return categories

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий"""
        return self._categories

""""
    def get_category_by_codename(self, category_name: str) -> str:
        found = None
        for category in self._categories:		
            if category['codename'] == category_name:
               found = category
               break
        return found			
"""