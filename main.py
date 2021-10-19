from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re
import MySQLdb.cursors
import yaml

import os
from werkzeug.utils import secure_filename
import shutil
from flask.helpers import send_file

from PixOps import super_resolution

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = '1234'
# db = yaml.load(open('SQL_Login.yaml'))
# Enter your database connection details below
# app.config['MYSQL_HOST'] = db['MYSQL_HOST']
# app.config['MYSQL_USER'] = db['MYSQL_USER']
# app.config['MYSQL_PASSWORD'] = db['MYSQL_PASSWORD']
# app.config['MYSQL_DB'] = db['MYSQL_DB']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qwerty'
app.config['MYSQL_DB'] = 'PixOpsUsers'



# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/login - this will be the login page, we need to use both GET and POST requests


@app.route('/')
def gotoLogin():
    return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = 'An error occured'
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM PixOpsAccounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('homepage'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg='')



@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM PixOpsAccounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO PixOpsAccounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    



@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        # clean_folders('./static/generated')
        # clean_folders('./uploads')
       
        return render_template('homepage.html')

 
#  MODULE 1 ---- SUPER RESOLUTION
@app.route('/super-resolution', methods=['GET', 'POST'])
def mod1():
    if request.method == 'GET':
        return render_template('mod1.html',outputShow=False)
   
    elif request.method == 'POST':
        uploadedPic = request.files['photoupload'] 
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static\\uploads', secure_filename("uploadedPicMod1.png"))
        uploadedPic.save(file_path)
        mod1 = super_resolution()
        # mod1.gen_sr(".//uploads//uploadedPicMod1.png")
        mod1.gen_sr(file_path)
    return render_template('mod1.html',outputShow=True)
    # return render_template('mod1.html')

@app.route('/download', methods=['GET', 'POST'])  
def mod1Download():
    if request.method == 'POST':   
        return send_file('static\generated\superImage.png',as_attachment='True')



# def clean_folders(file_path):
   
#     if os.path.isfile(file_path) or os.path.islink(file_path):
#         os.unlink(file_path)
#         os.mkdir(file_path)
#     elif os.path.isdir(file_path):
#         shutil.rmtree(file_path)
#         os.mkdir(file_path)
    
app.run(debug=True)