from flask import Flask, flash, render_template, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

from FDataBase import FDataBase
from UserLogin import UserLogin
from Chat import Chat


DATABASE = '/tmp/dbase.bd'
DEBUG = True
SECRET_KEY = 'jgfjlfkj765@68976,<34'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dbase.db')))
#app.config['SERVER_NAME'] = "0.0.0.0"

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dbase.db')))
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
curr_user = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "POST":
        global curr_user
        app.config.update(dict(DATABASE=os.path.join(app.root_path, 'users.db')))
        user = dbase.getUserByName(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['password']):
            curr_user = UserLogin().create(user)
            login_user(curr_user)
            return redirect("/profile")

    return render_template("login.html")


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 4 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect("/profile")
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html")


@app.route('/messenger')
@login_required
def messenger():
    return render_template("messenger.html")


@app.route('/personlist', methods=['POST', "GET"])
@login_required
def personlist():
    if request.method == "POST":
        if curr_user:
            user_1_id = UserLogin().create(dbase.getUserById(request.form['id'])).get_id()
            curr_user_id = curr_user.get_id()
            dbase.addChat("", curr_user_id, user_1_id)
        return redirect("/messenger")

    return render_template("personlist.html")


@app.route('/chat/<int:id>', methods=['POST', "GET"])
@login_required
def chat(id):
    chat = Chat().create(dbase.getChatById(id))

    if request.method == "POST":
        if curr_user:
            message = request.form['message']
            chat_id = chat.get_id()
            dbase.addMessage(chat_id, message)

    user0_id = chat.get_users_id().split()[0]
    user1_id = chat.get_users_id().split()[1]

    if curr_user.get_id() == user0_id:
        opponent_id = user1_id
    else:
        opponent_id = user0_id

    if not(user0_id == curr_user.get_id() or user1_id == curr_user.get_id()):
        return redirect("/messenger")

    all = []
    all.append(str(UserLogin().create(dbase.getUserById(opponent_id)).get_name()))
    messages_all = dbase.getMessagesByChatId(chat.get_id())
    messages = ""
    if messages_all:
        for message in messages_all:
            messages += '<br><span>' + message['text'] + '</span>'

    if not(messages):
        messages = ""

    all.append(messages)
    print(all)

    return render_template("chat.html").format(*all)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect("/login")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)


if __name__ == "__main__":
    app.run(host="", port=5000)
