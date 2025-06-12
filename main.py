from flask import Flask, render_template, request, g, flash, abort, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import time

from FDataBase import FDataBase
from UserLogin import UserLogin
from Chat import Chat


DATABASE = '/tmp/dbase.bd'
DEBUG = True
SECRET_KEY = 'jgfjlfkj765@68976,<34'

CHAT_REF = '''<a class="chat_ref__outer" href="/chat/{0}"><div class="chat_ref__outer"><div class="chat_ref__inner"><div class="chat_ref_avatar"><icon><img class="icon" src="/static/gallery/icons/profile.png" width="100%"></icon></div><div class="chat_ref_name">{1}</div></div></div></a>'''
RTL_MESSAGE = '''<div class="message_RTL"><div class="message__outer"><div class="message__avatar"></div><div class="message__inner"><div class="message__bubble__blue"><span>{0}</span></div><div class="message__actions"></div><div class="message__spacer"></div></div><div class="message__status"></div></div></div>'''
LTL_MESSAGE = '''<div class="message_LTL"><div class="message__outer"><div class="message__inner"><div class="message__spacer"></div><div class="message__actions"></div><div class="message__bubble__grey"><span>{0}</span></div></div><div class="message__avatar"></div></div></div>'''
FRIEND_REF = '''<a class="friends_list_ref__outer" href="/user/name={0}"><div class="friends_list_ref__outer"><div class="friends_list_ref__inner"><div class="universal_spacer"></div><div class="friends_list_ref__bubble"><div class="chat_ref_avatar"><icon><img class="icon" src="/static/gallery/icons/profile.png" width="100%"></icon></div><div class="chat_ref_name">{1}</div></div><div class="universal_spacer"></div></div></div></a>'''
FRIEND_REF_CHAT = '''<a class="friends_list_ref__outer" href="/newchat/{0}"><div class="friends_list_ref__outer"><div class="friends_list_ref__inner"><div class="universal_spacer"></div><div class="friends_list_ref__bubble"><div class="chat_ref_avatar"><icon><img class="icon" src="/static/gallery/icons/profile.png" width="100%"></icon></div><div class="chat_ref_name">{1}</div></div><div class="universal_spacer"></div></div></div></a>'''
POST = '''<a class="post" href="/watch/post={0}"><div class="post"><div class="post__outer"><div class="post__inner"><div class="post__sender__outer"><div class="post__sender__inner"><div class="post__sender__bubble"><div class="post__sender"><span>{1}</span></div><div class="universal_spacer"></div><div class="post__time"><span>{2}</span></div><div class="vertical_line"></div><div class="post__date"><span>{3}</span></div></div></div></div><div class="universal_spacer"></div><div class="post__body__outer"><div class="post__body__inner"><div class="post__body__bubble"><span>{4}</span></div></div></div><div class="universal_spacer"></div><div class="post__footer__outer"><div class="post__footer__inner"><div class="post__footer__bubble"><div class="post__views__outer"><div class="post__views__inner"><icon><img src="/static/gallery/icons/views.png" width="100%"></icon><div class="post__views__text"><span>{5}</span></div></div></div><div class="universal_spacer"></div><div class="post__commentaries__outer"><div class="post__commentaries__inner"><div class="post__commentaries__text"><span>1k</span></div><icon><img src="/static/gallery/icons/commentaries.png" width="100%"></icon></div></div></div></div></div></div></div></div></a>'''
POST_WITHOUT_REF = '''<div class="post"><div class="post__outer"><div class="post__inner"><div class="post__sender__outer"><div class="post__sender__inner"><div class="post__sender__bubble"><a class="post__sender" href="/user/name={0}"><div class="post__sender"><span>{1}</span></div></a><div class="universal_spacer"></div><div class="post__time"><span>{2}</span></div><div class="vertical_line"></div><div class="post__date"><span>{3}</span></div></div></div></div><div class="universal_spacer"></div><div class="post__body__outer"><div class="post__body__inner"><div class="post__body__bubble"><span>{4}</span></div></div></div><div class="universal_spacer"></div><div class="post__footer__outer"><div class="post__footer__inner"><div class="post__footer__bubble"><div class="post__views__outer"><div class="post__views__inner"><icon><img src="/static/gallery/icons/views.png" width="100%"></icon><div class="post__views__text"><span>{5}</span></div></div></div><div class="universal_spacer"></div><div class="post__commentaries__outer"><div class="post__commentaries__inner"><div class="post__commentaries__text"><span>1k</span></div><icon><img src="/static/gallery/icons/commentaries.png" width="100%"></icon></div></div></div></div></div></div></div></div>'''


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

    all = []
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

        friends = dbase.getUserFriends(current_user.get_id())
        friends_refs = ""
        if friends:
            for _friend_id in friends:
                _friend = dbase.getUserById(_friend_id)
                _friend_user_name = str(_friend['username'])
                friends_refs += FRIEND_REF_CHAT.format(_friend['id'], _friend_user_name)

    all.append(chat_refs)
    all.append(friends_refs)

    return render_template("personlist.html").format(*all)


@app.route('/newchat/<int:id>')
@login_required
def newchat(id):
    if current_user:
        user_1_id = id
        if not(dbase.getChatByUsersId(int(current_user.get_id()), user_1_id)) and (int(current_user.get_id()) != int(user_1_id)):
            dbase.addChat("", int(current_user.get_id()), int(user_1_id))
            _chat = dbase.getChatByUsersId(int(current_user.get_id()), int(user_1_id))['id']
            return redirect("/chat/{0}".format(_chat))

    return redirect("/messenger")


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


@app.route('/friendslist', methods=['POST', "GET"])
@login_required
def friendslist():
    if request.method == "POST":
        if current_user:
            friend_id = dbase.getUserByName(request.form['username'])['id']
            print(friend_id)
            if not (friend_id in dbase.getUserFriends(current_user.get_id())) and int(current_user.get_id()) != int(friend_id):
                dbase.addUserFriend(int(current_user.get_id()), int(friend_id))
                dbase.addUserFriend(int(friend_id), int(current_user.get_id()))
        return redirect("/friendslist")

    friend_refs = ""
    if current_user:
        friends = dbase.getUserFriends(current_user.get_id())
        if friends:
            for friend in friends:
                print("friend_id = " + str(friend))
                _friend_user_name = str(dbase.getUserById(friend)['username'])
                friend_refs += FRIEND_REF.format(_friend_user_name, _friend_user_name)

    return render_template("friendslist.html").format(friend_refs)


@app.route('/watch/post=<int:id>', methods=['POST', "GET"])
@login_required
def post(id):
    if current_user:
        _post = dbase.getPostById(id)
        if _post:
            all = []
            dbase.addViewToPost(id, int(current_user.get_id()))

            _views_list = list((str(_post['views'])[1:-1]).split(', '))
            if _views_list == ['']:
                _views_count = 0
            else:
                _views_count = len(list(map(int, _views_list)))

            if _views_count >= 1000:
                _views_count = str(str(_views_count // 1000) + "k")

            post_time = _post['time']
            _post_time = time.localtime(post_time)
            _sender = dbase.getUserById(_post['sender'])
            post = POST_WITHOUT_REF.format(_sender['username'], _sender['username'], time.strftime('%d.%m.%Y', _post_time), time.strftime('%H:%M', _post_time), _post['text'], _views_count)

            all.append(_sender['username'])
            all.append(time.strftime('%d.%m.%Y %H:%M', _post_time))
            all.append(post)

            return render_template("post.html").format(*all)

    return redirect("/")


@app.route('/new_post', methods=['POST', "GET"])
@login_required
def new_post():
    if request.method == "POST":
        if current_user:
            post_text = request.form['text']
            dbase.addPost(current_user.get_id(), post_text)
            return redirect("/profile")

    return render_template("new_post.html")


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
    all = []
    _posts_list = ""
    if current_user:
        _posts = dbase.getPostsByUserId(current_user.get_id())
        if _posts:
            for _post in _posts:
                post_time = _post['time']
                _post_time = time.localtime(post_time)

                _views_list = list((str(_post['views'])[1:-1]).split(', '))
                if _views_list == ['']:
                    _views_count = 0
                else:
                    _views_count = len(list(map(int, _views_list)))

                if _views_count >= 1000:
                    _views_count = str(str(_views_count // 1000) + "k")

                _posts_list = POST.format(_post['id'], current_user.get_name(), time.strftime('%d.%m.%Y', _post_time), time.strftime('%H:%M', _post_time), _post['text'], _views_count) + _posts_list

    all.append(_posts_list)

    return render_template("profile.html").format(*all)


@app.route('/user/name=<string:username>')
def user(username):
    all = []
    _posts_list = ""
    if current_user:
        _user = dbase.getUserByName(username)
        if _user:
            if int(_user['id']) == int(current_user.get_id()):
                return redirect("/profile")
            _posts = dbase.getPostsByUserId(_user['id'])
            if _posts:
                for _post in _posts:
                    post_time = _post['time']
                    _post_time = time.localtime(post_time)

                    _posts_list = POST.format(_post['id'], _user['username'], time.strftime('%d.%m.%Y', _post_time),
                                              time.strftime('%H:%M', _post_time), _post['text']) + _posts_list

    all.append(_posts_list)
    return render_template("profile.html").format(*all)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
