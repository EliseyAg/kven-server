import math
import sqlite3
import time


class ChatsDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addChat(self, name,  user0id, user1id):
        try:
            self.__cur.execute("INSERT INTO chats VALUES(NULL, ?, ?, ?)", (name, user0id, user1id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

    def getChatByName(self, chat_name):
        try:
            self.__cur.execute(f"SELECT * FROM chats WHERE name = '{chat_name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
