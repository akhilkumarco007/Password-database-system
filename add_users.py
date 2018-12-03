import random
import sqlite3

from utils import generate_password, create_user


def add_users(count) -> None:
    """Retrieve 10 users and generate passwords for each user

     Save the name, email and password in a sqlite database

    :return: None
    """
    for _ in range(count):
        create_user('user_info.db')

    with sqlite3.connect('user_info.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_name = cursor.fetchall()[0][0]
        try:
            cursor.execute("ALTER TABLE " + table_name + " ADD COLUMN password")
        except sqlite3.OperationalError:
            pass
        finally:
            for i in range(1, count + 1):
                cursor.execute("UPDATE " + table_name + " SET password=? WHERE id=?",
                               (generate_password(random.choice(range(6, 13)), random.choice(range(1, 5))), i))


if __name__ == '__main__':
    add_users(10)
