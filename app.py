import hashlib
from flask import Flask, request, render_template, flash, redirect, url_for, session
import settings
from db import get_user, enter_infos, get_tasks, insert_task, delete_task, get_task_by_id



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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' in session:
        if request.method == 'GET':
            return render_template('profile.html', html_tasks=get_tasks(session['user']))

        if request.method == "POST":
            insert_task(
                title=request.form['title'],
                description=request.form['description'],
                user_id=session['user']
            )
            return render_template('profile.html', html_tasks=get_tasks(session['user']))

    else:
        return redirect(url_for('login'))
    
    
@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = next((task for task in get_tasks(session['user']) if task['id'] == task_id))
    if task:
        return render_template("task_detail.html", task=task)
    return "Task topilmadi"

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    if delete_task(task_id):
        flash("Task o'chirildi!")
        return redirect(url_for('profile'))
    else:
        flash("Task topilmadi.")
        return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
