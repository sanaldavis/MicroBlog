from flask import *
from time import *
import sqlite3 as lite

app=Flask(__name__)
app.secret_key = 'sanu'

@app.route('/')
def welcome():
	return render_template('home.html')

@app.route('/home')
def home():
	con=lite.connect('database.db')
        cur=con.cursor()
        cur.execute("SELECT * FROM blog_database ORDER BY id desc")
	post = [ dict ( id = i[0], author = i[1], post = i[2], day = i[3], time = i[4] ) for i in cur.fetchall() ]
        con.commit()
        con.close()
	if 'logged_in' in session:
		return render_template('home_logout.html', post = post)
	else:
		return render_template('home.html', post = post)

@app.route('/post')
def post():
	if 'logged_in' in session:
		return render_template('post.html')
	else:
		return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
def post_store():
	con=lite.connect('database.db')
	cur=con.cursor()
	cur.execute("INSERT INTO blog_database(author, post, day, time) VALUES(?,?,?,?)", [ request.form['name'], request.form['blogpost'], strftime( "%d %b %Y" , gmtime()), strftime( "%H:%M:%S", gmtime())]) 
	con.commit()
	con.close()
	return render_template('post.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'sanal' and request.form['password'] == 'tharayil':
			session['logged_in'] = True
			return redirect(url_for('post'))
		else:
			error = 'Please check username and password'

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None )
	return redirect(url_for('login'))

app.run(debug = True)


