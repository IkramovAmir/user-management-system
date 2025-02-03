import hashlib
from flask import Flask, request, render_template, flash, redirect, url_for, session
import settings
from db import get_user, enter_infos


app = Flask(__name__)
app.secret_key = settings.secret_key

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form

        user = get_user(form['username'])
        if user:
            flash("Siz tanlagan username mavjud.")
            return render_template('register.html')

        enter_infos(
            form['name'], 
            form['username'], 
            hashlib.sha256(form['password'].encode()).hexdigest()
        )

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username) # user obj or None
        if user is None:
            flash("User mavjud emas, royxatdan o'tish")
            return render_template('login.html')

        if user[3] != hashlib.sha256(password.encode()).hexdigest():
            flash("password xato kiritdingiz.")
            return render_template('login.html')

        session['user'] = user[0]

        return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' in session:
        return "profile page"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
