# Store this code in 'app.py' file

import email
from sqlite3 import Time
from telnetlib import NOP
from time import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


#app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'travelbuddy'

mysql = MySQL(app)

@app.route('/')
def home():
   return render_template('mainindex.html')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('mainindex.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'fullname' in request.form and 'cmp' in request.form and 'in' in request.form and 'dl' in request.form and 'age' in request.form and 'pn' in request.form and 'gender' in request.form:
		email = request.form['email']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		name=request.form['fullname']
		cmp=request.form['cmp']
		inumber=request.form['in']
		dl=request.form['dl']
		Age=request.form['age']
		pn=request.form['pn']
		Gender=request.form['gender']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM signup_driver WHERE Email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', inumber):
			msg = 'Insurance number must contain only characters and numbers !'
		elif not re.match(r'[0-9]+', dl):
			msg = 'Driving Licence Number  must contain only numbers !'
		elif not re.match(r'[0-9]+', Age):
			msg = 'Age  must contain only numbers !'
		elif not re.match(r'[0-9]+',pn):
			msg = 'pn  must contain only numbers !'
		elif not re.match(r'[A-Za-z]+', Gender):
			msg = 'Gender  must contain only characters !'
		elif not Gender or not pn or not Age or not cmp or not inumber or not dl or not confirmpassword or not name or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO signup_driver VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (name, email, password, inumber , dl, cmp,Age,Gender,pn))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('post_ride.html', msg = msg)

@app.route('/post_ride', methods =['GET', 'POST'])
def registernew():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'fullname' in request.form  and  'age' in request.form and 'pn' in request.form and 'gender' in request.form:
		email = request.form['email']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		name=request.form['fullname']
		Age=request.form['age']
		pn=request.form['pn']
		Gender=request.form['gender']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM signup_passenger WHERE Email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'

		elif not re.match(r'[0-9]+', Age):
			msg = 'Age  must contain only numbers !'
		elif not re.match(r'[0-9]+',pn):
			msg = 'pn  must contain only numbers !'
		elif not re.match(r'[A-Za-z]+', Gender):
			msg = 'Gender  must contain only characters !'
		elif not Gender or not pn or not Age or not confirmpassword or not name or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO signup_passenger VALUES (NULL, % s, % s, % s, % s, % s, % s)', (name, email, password ,Age, Gender, pn))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('rides.html', msg = msg)



if __name__ == '__main__':
   app.run()

	
