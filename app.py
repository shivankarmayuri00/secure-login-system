from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password BLOB
    )
    ''')
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('users.db')
        conn.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        user = conn.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return redirect('/dashboard')

        return "Invalid Login ❌"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)