import sqlite3

def create_db():
    db = sqlite3.connect('database/users.db')
    cursor = db.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, 
                        login TEXT, 
                        encodings BLOB);''')

    db.close()

def check_username(username):
    db = sqlite3.connect('database/users.db')
    cursor = db.cursor()

    cursor.execute('SELECT login FROM users WHERE login = ?', (username,))
    flag = cursor.fetchone() is None

    cursor.close()
    db.close()

    return flag

def add_user(username, encodings):
    db = sqlite3.connect('database/users.db')
    cursor = db.cursor()

    cursor.execute('INSERT INTO users (login, encodings) VALUES (?, ?)', (username, encodings))
    db.commit()
    print(f'User [{username}] has been successfully registered\n')

    cursor.close()
    db.close()

def get_info():
    db = sqlite3.connect('database/users.db')
    cursor = db.cursor()

    cursor.execute('SELECT login, encodings FROM users')
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return users


