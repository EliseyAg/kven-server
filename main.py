from flask import Flask, flash, render_template, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

from FDataBase import FDataBase
from UserLogin import UserLogin


#DATABASE = '/tmp/users.bd'
DEBUG = True
SECRET_KEY = 'jgfjlfkj765@68976,<34'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'users.db')))
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'chats.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db(DATABASE):
    conn = sqlite3.connect(app.config[DATABASE])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("chats_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db(DATABASE):
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db('DATABASE')
    return g.link_db


dbase = None
dbase_chats = None


@app.before_request
def before_request():
    global dbase
    global dbase_chats
    db = get_db('/tmp/users.bd')
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
        user = dbase.getUserByName(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
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
def personlist():
    if request.method == "POST":
        pass

    return render_template("personlist.html")


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
@login_required
def profile():
    return render_template("profile.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)


if __name__ == "__main__":
    app.run()
