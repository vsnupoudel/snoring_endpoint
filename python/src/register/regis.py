# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, os
from storage import util
from flask_pymongo import PyMongo
import gridfs

app = Flask(__name__)

app.secret_key = 'TODO'

app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config["MYSQL_PORT"] =  int( os.environ.get("MYSQL_PORT"))
app.config['MYSQL_DB'] =  os.environ.get("MYSQL_DB")

mysql = MySQL(app)

# mongo_wav = PyMongo(
#         app,
#         uri= "mongodb://adminuser:password123@{}/wav?authSource=admin".format(os.environ.get("MONGO_SVC_ADDRESS"))
# 					)
print( "{}".format(os.environ.get("MONGO_SVC_ADDRESS")) )
mongo_wav = PyMongo(
        app,
        uri= "{}".format(os.environ.get("MONGO_SVC_ADDRESS"))
					)
print('mongo_wav:', mongo_wav)
fs_wav = gridfs.GridFS(mongo_wav.db)

@app.route('/')
@app.route('/login', methods =['GET' ,'POST'])
def login():
	msg = 'Login page'
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
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
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/upload' , methods=['GET','POST'])
def upload():
	msg = 'Please upload the audio file'
	if request.method == 'POST':
			fileObjects = request.files.getlist('file')			
			filenames = [ util.upload(fs_wav, fileObj)  for fileObj in fileObjects ]
			return render_template('upload.html', msg = filenames) 
	return  render_template('upload.html', msg = msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
