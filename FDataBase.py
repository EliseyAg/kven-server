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
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (username, hashpass, "[]", tm))
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

    def getUserFriends(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Чат не найден")
                return False

            _friends_array = list((str(res['friends_id'])[1:-1]).split(', '))
            if _friends_array == ['']:
                friends_array = []
            else:
                friends_array = list(map(int, _friends_array))
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return friends_array

    def addUserFriend(self, user_id, friend_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Чат не найден")
                return False

            _friends_array = list((str(res['friends_id'])[1:-1]).split(', '))
            if _friends_array == ['']:
                friends_array = []
            else:
                friends_array = list(map(int, _friends_array))
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        friends_array.append(friend_id)

        try:
            self.__cur.execute(f"UPDATE users SET friends_id = '{friends_array}' WHERE id = '{user_id}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

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

    def getChatByUsersId(self, user0_id, user1_id):
        try:
            self.__cur.execute(f"SELECT * FROM chats WHERE (user_id0 = '{user0_id}' AND user_id1 = '{user1_id}') OR (user_id1 = '{user0_id}' AND user_id0 = '{user1_id}')")
            res = self.__cur.fetchone()

            if not res:
                print("Чаты не найдены")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getChatsByUserId(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM chats WHERE user_id0 = '{user_id}' OR user_id1 = '{user_id}'")
            row = self.__cur.fetchone()
            res = []
            while row is not None:
                res.append(row)
                row = self.__cur.fetchone()

            if not res:
                print("Чаты не найдены")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addMessage(self, user_id, chat_id, text, tp, reply_id=-1):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO messages VALUES(NULL, ?, ?, ?, ?, ?, ?)", (user_id, chat_id, text, reply_id, tp, tm))
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

    def addPost(self, user_id, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?, ?)",
                               (user_id, text, "[]", "[]", tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД: " + str(e))
            return False

        return True

    def addViewToPost(self, post_id, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM posts WHERE id = '{post_id}'")
            res = self.__cur.fetchone()
            if not res:
                print("Пост не найден")
                return False

            _views_array = list((str(res['views'])[1:-1]).split(', '))
            if _views_array == ['']:
                views_array = []
            else:
                views_array = list(map(int, _views_array))

            if not(user_id in views_array):
                views_array.append(user_id)

        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
            return False

        try:
            print(views_array)
            self.__cur.execute(f"UPDATE posts SET views = '{views_array}' WHERE id = '{post_id}'")
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка обновления данных в БД " + str(e))

        return True

    def getPostsByUserId(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM posts WHERE sender = '{user_id}'")
            row = self.__cur.fetchone()
            res = []
            while row is not None:
                res.append(row)
                row = self.__cur.fetchone()
            if not res:
                print("Пост не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getPostById(self, post_id):
        try:
            self.__cur.execute(f"SELECT * FROM posts WHERE id = '{post_id}'")
            res = self.__cur.fetchone()
            if not res:
                print("Пост не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getAllPosts(self):
        try:
            self.__cur.execute(f"SELECT * FROM posts")
            row = self.__cur.fetchone()
            res = []
            while row is not None:
                res.append(row)
                row = self.__cur.fetchone()

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def addCommentaryToPost(self, type, id, reply, sender, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO commentary VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)", (type, id, reply, sender, text, "[]", tm))
            self.__db.commit()

            return True
        except sqlite3.Error as e:
            print("Ошибка добавления данных в БД " + str(e))

        return False

    def getCommentariesByPostId(self, post_id):
        try:
            self.__cur.execute(f"SELECT * FROM commentary WHERE post_id = '{post_id}'")
            row = self.__cur.fetchone()
            res = []
            while row is not None:
                res.append(row)
                row = self.__cur.fetchone()
            if not res:
                print("Пост не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
