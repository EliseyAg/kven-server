CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    psw text NOT NULL,
    friends_id string,
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
    sender integer NOT NULL,
    chat_id NOT NULL,
    text text NOT NULL,
    reply_id integer NULL,
    type text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS commentary (
    id integer PRIMARY KEY AUTOINCREMENT,
    is_reply bool NOT NULL,
    post_id integer NOT NULL,
    sender text NOT NULL,
    likes integer NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS video (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    len integer NOT NULL,
    views integer NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    sender integer NOT NULL,
    text text NOT NULL,
    type text NOT NULL,
    views integer NOT NULL,
    time integer NOT NULL
);
