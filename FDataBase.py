import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, username,  hashpass):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, hashpass, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

    def getUserById(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getUserByName(self, user_name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = '{user_name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addChat(self, name,  user0id, user1id):
        try:
            self.__cur.execute("INSERT INTO chats VALUES(NULL, ?, ?, ?)", (name, user0id, user1id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

    def getChatById(self, chat_id):
        try:
            self.__cur.execute(f"SELECT * FROM chats WHERE id = '{chat_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Чат не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getChatByName(self, chat_name):
        try:
            self.__cur.execute(f"SELECT * FROM chats WHERE name = '{chat_name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Чат не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addMessage(self, chat_id, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO messages VALUES(NULL, ?, ?, ?)", (chat_id, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

    def getMessagesByChatId(self, chat_id):
        try:
            self.__cur.execute(f"SELECT * FROM messages WHERE chat_id = '{chat_id}'")
            row = self.__cur.fetchone()
            res = []
            while row is not None:
                res.append(row)
                row = self.__cur.fetchone()
            if not res:
                print("Сообщение не найдено")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
