from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'userbase'
}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['password']
    # Check if the user exists and if the password matches
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        return f'Logged in with {user[2]}'
    else:
        return "Invalid username or password"


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['uname']
    email = request.form['email']
    password = request.form['password']
    # Check if the username already exists
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Username already exists"
    else:
        # Insert the new user into the database
        insert_query = "INSERT INTO users (username, email,password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, email, password))
        connection.commit()
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
