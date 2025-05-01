class Chat():
    def fromDB(self, chat_id, db):
        self.__chat = db.getChatById(chat_id)
        return self

    def create(self, chat):
        self.__chat = chat
        return self

    def get_id(self):
        return str(self.__chat['id'])

    def get_users_id(self):
        return str(self.__chat['user_id0'] + ' ' + self.__chat['user_id1'])
