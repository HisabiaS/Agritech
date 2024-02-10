from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import re  # For regular expression operations
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Function to check if the user exists in the CSV
def user_exists(username):
    with open('users.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:
                return True
    return False

# Function to validate password complexity
def is_password_valid(password):
    if len(password) < 8:
        return False
    if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
        return False
    return True

# Function to validate user login
def validate_user_login(username, password):
    with open('users.csv', mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indexmain')
def indexmain():
    return render_template('indexmain.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash('Both username and password are required.', 'error')
            return redirect(url_for('signup'))
        elif not is_password_valid(password):
            flash('Password must be at least 8 characters long and contain both letters and numbers.', 'error')
            return redirect(url_for('signup'))
        elif user_exists(username):
            flash('Username already exists. Please log in.', 'info')
            return redirect(url_for('login'))
        else:
            with open('users.csv', mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, password])
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Both username and password are required.', 'error')
            return redirect(url_for('login'))
        elif validate_user_login(username, password):
            return render_template('News.html')
        else:
            flash('Login failed. Invalid username or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()  # Wait 1 second before opening the web browser
    app.run(debug=True)
