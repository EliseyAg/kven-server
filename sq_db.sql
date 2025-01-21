CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    psw text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS chats (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    user_id0 text NOT NULL,
    user_id1 text NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY AUTOINCREMENT,
    chat_id NOT NULL,
    text text NOT NULL,
    time integer NOT NULL
);
