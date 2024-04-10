import sqlite3
"""CRUD"""


def get_all(db) -> list:
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    SELECT *
                    FROM employee            
        """

        cursor.execute(query)

        return cursor.fetchall()


def get_one(db, surname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = f"""SELECT * 
                    FROM employee 
                    WHERE surname = '{surname}'"""

        cursor.execute(query)

        return cursor.fetchall()


