from flask import Flask, flash, render_template, request, redirect, g, url_for
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

CHAT_REF = '''<a class="chat_ref__outer" href="/chat/{0}"><div class="chat_ref__outer"><div class="chat_ref__inner"><div class="chat_ref_avatar"><icon><img class="icon" src="/static/gallery/icons/profile.png"/ width="100%"></icon></div><div class="chat_ref_name">{1}</div></div></div></a>'''
RTL_MESSAGE = '''<div class="message_RTL"><div class="message__outer"><div class="message__avatar"></div><div class="message__inner"><div class="message__bubble__blue"><span>{0}</span></div><div class="message__actions"></div><div class="message__spacer"></div></div><div class="message__status"></div></div></div>'''
LTL_MESSAGE = '''<div class="message_LTL"><div class="message__outer"><div class="message__inner"><div class="message__spacer"></div><div class="message__actions"></div><div class="message__bubble__grey"><span>{0}</span></div></div><div class="message__avatar"></div></div></div>'''


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dbase.db')))
#app.config['SERVER_NAME'] = "0.0.0.0"

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    print("load user")
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
    if current_user.is_authenticated:
        return redirect("/profile")

    if request.method == "POST":
        user = dbase.getUserByName(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['password']):
            user_login = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(user_login, remember=rm)
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
                user = dbase.getUserByName(request.form['username'])
                user_login = UserLogin().create(user)
                rm = True if request.form.get('remainme') else False
                login_user(user_login, remember=rm)
                return redirect("/profile")
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html")


@app.route('/messenger')
@login_required
def messenger():
    chat_refs = ""
    if current_user:
        chats = dbase.getChatsByUserId(current_user.get_id())
        if chats:
            for _chat in chats:
                _user0_id = _chat['user_id0']
                _user1_id = _chat['user_id1']

                if current_user.get_id() == _user0_id:
                    _opponent_id = _user1_id
                else:
                    _opponent_id = _user0_id

                _opponent_user_name = str(dbase.getUserById(_opponent_id)['username'])
                chat_refs += CHAT_REF.format(_chat['id'], _opponent_user_name)

    return render_template("messenger.html").format(chat_refs)


@app.route('/personlist', methods=['POST', "GET"])
@login_required
def personlist():
    if request.method == "POST":
        if current_user:
            user_1_id = dbase.getUserById(request.form['id'])['id']
            if not(dbase.getChatByUsersId(current_user.get_id(), user_1_id)) and current_user.get_id() != user_1_id:
                dbase.addChat("", current_user.get_id(), user_1_id)
        return redirect("/messenger")

    chat_refs = ""
    if current_user:
        chats = dbase.getChatsByUserId(current_user.get_id())
        if chats:
            for _chat in chats:
                _user0_id = _chat['user_id0']
                _user1_id = _chat['user_id1']

                if current_user.get_id() == _user0_id:
                    _opponent_id = _user1_id
                else:
                    _opponent_id = _user0_id

                _opponent_user_name = str(dbase.getUserById(_opponent_id)['username'])
                chat_refs += CHAT_REF.format(_chat['id'], _opponent_user_name)

    return render_template("personlist.html").format(chat_refs)


@app.route('/chat/<int:id>', methods=['POST', "GET"])
@login_required
def chat(id):
    chat = Chat().create(dbase.getChatById(id))

    if request.method == "POST":
        if current_user:
            message = request.form['message']
            if message != "":
                chat_id = chat.get_id()
                dbase.addMessage(current_user.get_id(), chat_id, message, "TEXT")

    user0_id = chat.get_users_id().split()[0]
    user1_id = chat.get_users_id().split()[1]

    if current_user.get_id() == user0_id:
        opponent_id = user1_id
    else:
        opponent_id = user0_id

    if not(user0_id == current_user.get_id() or user1_id == current_user.get_id()):
        return redirect("/messenger")

    all = []

    chat_refs = ""
    chats = dbase.getChatsByUserId(current_user.get_id())

    if chats:
        for _chat in chats:
            _user0_id = _chat['user_id0']
            _user1_id = _chat['user_id1']

            if current_user.get_id() == _user0_id:
                _opponent_id = _user1_id
            else:
                _opponent_id = _user0_id

            _opponent_user_name = str(dbase.getUserById(_opponent_id)['username'])
            chat_refs += CHAT_REF.format(_chat['id'], _opponent_user_name)

    all.append(chat_refs)

    opponent_user_name = str(dbase.getUserById(opponent_id)['username'])
    all.append(opponent_user_name)

    messages_all = dbase.getMessagesByChatId(chat.get_id())
    messages = ""
    if messages_all:
        for message in messages_all:
            if message['sender'] == int(current_user.get_id()):
                messages += RTL_MESSAGE.format(message['text'])
            else:
                messages += LTL_MESSAGE.format(message['text'])

    if not(messages):
        messages = ""

    all.append(messages)

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
    app.run(host="0.0.0.0", port=5000)
