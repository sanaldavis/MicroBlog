import sqlite3 as lite
con=None
con=lite.connect('database.db')
cur=con.cursor()
cur.execute('''CREATE TABLE blog_database( id integer primary key autoincrement, author text, post text, day text, time text, comment text)''')
con.commit()
con.close()

