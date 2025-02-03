import mysql.connector
import settings

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id int auto_increment primary key, 
    title varchar(128) not null,
    description varchar(512) not null,
    user_id int not null
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
    cursor.execute("select * from tasks where user_id=%s", (user_id,))
    return cursor.fetchall()
    