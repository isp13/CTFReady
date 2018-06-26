from flask import Flask, render_template, request, make_response, redirect, render_template_string, config
import sqlite3
from hashlib import md5
import os


app = Flask(__name__)

f = os.path.join(os.path.abspath(os.path.dirname(__file__)),'example.db') #Local file
conn = sqlite3.connect(f)
db = conn.cursor()
SECRET_NUM = 1337


def hash_string(s):
    s = s.encode()
    return md5(s).hexdigest()


def get_login(id):
    query = 'SELECT login FROM users WHERE id = {}'.format(id)
    db.execute(query)
    result = db.fetchone()
    if result is None:
        return None
    else:
        return result[0]


def get_notes(id):
    query = 'SELECT text FROM notes WHERE creator_id = {}'.format(id)
    result = []
    for row in db.execute(query):
        result.append(row[0])
    return result


def check_login(user):
    query = 'SELECT * FROM users WHERE login = "{}"'.format(user)
    db.execute(query)
    exist = db.fetchone()
    if exist is None:
        return False
    else:
        return True


@app.route('/user')
def user():
    id = request.cookies.get('id',None)
    if 'id' is None:
        return render_template('user.html')
    login = get_login(id)
    if not login:
        return "Page is not longer avialable"

    return render_template('user.html', username=login, notes=get_notes(id), id=id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        if login == '' or password == '':
            return "Login or password is missing"
        password = hash_string(password)
        query = 'SELECT * FROM users WHERE login = "{}" and password = "{}"'.format(login, password)
        db.execute(query)
        result = db.fetchone()
        if result is None:
            return "No such user or password incorrect"
        resp = redirect('/user')
        resp.set_cookie('id',str(result[0]))
        return resp


@app.route('/add_note', methods=['POST'])
def add_note():
    id = request.cookies.get('id',None)
    if 'id' is None:
        return redirect('/')
    text = request.form.get('note', '')
    text = text.encode('utf-8', 'replace')
    if text == '':
        return "Empty note"
    query = 'INSERT INTO notes (text, creator_id) VALUES ("{}",{})'.format(text,id)
    db.execute(query)
    conn.commit()
    return redirect('/user')


@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')

        if login == '' or password == '':
            return "Login or password is missing"

        if check_login(login):
            return "This login already exist"

        password = hash_string(password)
        print(login,password)
        query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(login, password)
        db.execute(query)
        conn.commit()
        return "Success"

@app.errorhandler(404)
def page_not_found(e):
    template = '''
    <html>
    <head>
    <meta charset="UTF-8">
    <title>404</title>
    </head>
    <body>
    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>%s</h3>
    </div>
    </body>
    </html> ''' % (request.url)
    return render_template_string(template), 404

if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,login text,password text)'
    db.execute(init_query)
    init_query = 'CREATE TABLE IF NOT EXISTS notes(id  integer NOT NULL PRIMARY KEY AUTOINCREMENT,text text,creator_id integer)'
    db.execute(init_query)
    conn.commit()
    app.run(host="0.0.0.0", port=5005)
