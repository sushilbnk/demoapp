from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)


# Determine the database path
if 'WEBSITE_HOSTNAME' in os.environ:  # Running in Azure
    DB_PATH = os.path.join('/home/', 'database.db')
else:  # Running locally
    DB_PATH = os.path.join(os.getcwd(), 'database.db')


# Home Route (Login Page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vulnerable SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = cursor.execute(query).fetchone()
        conn.close()
        if result:
            return redirect('/dashboard')
        else:
            return "Login Failed (Try SQL Injection!)"
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Add User Route
@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vulnerable SQL query
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return "<script>alert('User added successfully!')</script>"
    return render_template('adduser.html')

# View Users Route
@app.route('/viewusers')
def view_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Vulnerable query to fetch users
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return render_template('viewusers.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
