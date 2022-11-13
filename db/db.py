"""Работа с БД"""
import os
from typing import Dict, List, Tuple

import sqlite3


conn = sqlite3.connect(os.path.join("db", "finance.db"))  # if not exists
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} " f"({columns}) " f"VALUES ({placeholders})", values
    )
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:  # TODO: naming
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetchsumforcurrentyear(table: str) -> float:
    cursor.execute(
        f"select sum(amount) FROM {table} where created > date('now','start of year')"
    )
    sum = cursor.fetchone()[0]
    return sum


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("db_init.sql", mode="r", encoding="utf-8") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute(
        "SELECT name FROM sqlite_master " "WHERE type='table' AND name='expense'"
    )
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()