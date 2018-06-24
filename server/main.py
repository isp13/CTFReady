from flask import Flask, request, render_template, redirect, make_response
import hashlib
app = Flask(__name__)

users = []

user_data = {}


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        login = request.form.get("login", "")
        password = request.form.get("password", "")
        if login == "" or password == "":
            return "Не были введены оба поля"

        users.append({"login": login, "password": hashlib.md5(password.encode()).hexdigest()})
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        login = request.form.get("login", "")
        password = hashlib.md5((request.form.get("password", "")).encode()).hexdigest()

        if login == "" or password == "":
            return "Не были введены оба поля"
        for user in users:
            if user["login"] == login and user["password"] == password:
                response = make_response(redirect("/"))
                response.set_cookie("login", login)
                response.set_cookie("password", password)
                return response
        return "Такого пользователя не существует"
    
    return render_template('login.html')


@app.route("/", methods=["POST", "GET"])
def index():
    login = request.cookies.get("login", "")
    password=request.cookies.get("password", "")
    for user in users:
        if user["login"] == login and user["password"] == password:
            secret = user_data.get(login, "")
            return render_template("index.html", name=login, secret=secret)
    if login=='' and password=='':
        return redirect("/register")
    else:
        return redirect("/login")



@app.route("/add_secret", methods=["POST", "GET"])
def secret():
    login = request.cookies.get("login", "")
    if login == "":
        return "NO-SYSTEM LOGIN"
    if request.method == "POST":
        secret = request.form.get("secret", "")
        user_data[login] = secret
        return redirect("/")
    else:
        return render_template("secret.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug=True, port=5003)
