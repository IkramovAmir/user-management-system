import mysql.connector
import settings, sqlite3

connection = mysql.connector.connect(
    user=settings.user,
    password=settings.password,
)

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS users_db")
cursor.execute("USE users_db")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id int auto_increment primary key, 
    name varchar(64) not null, 
    username varchar(64) not null, 
    password varchar(255) not null
);""")

def get_user(username):
    cursor.execute("select * from users where username=%s", (username, ))
    
    user = cursor.fetchone()
    if user:
        return user

    return None

def enter_infos(name, username, password):
    cursor.execute("insert into users (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    connection.commit()
    
def insert_task(title, description, user_id):
    cursor.execute("insert into tasks (title, description, user_id) VALUES (%s, %s, %s)", (title, description, user_id))
    connection.commit()

def get_tasks(user_id):
    cursor.execute("SELECT * FROM tasks WHERE user_id=%s", (user_id,))
    tasks = cursor.fetchall()
    return [{"id": task[0], "title": task[1], "description": task[2]} for task in tasks]


def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()

    if cursor.rowcount > 0:
        return True
    else:
        return False


def get_task_by_id(task_id):
    cursor.execute("SELECT id, title, description FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    if task:
        return {"id": task[0], "title": task[1], "description": task[2]}
    return None