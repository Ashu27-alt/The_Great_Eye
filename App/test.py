import sqlite3

db_path='/Users/ashutosh/processed.db'

conn=sqlite3.connect(db_path)
c=conn.cursor()
l=c.execute("SELECT * FROM processed")
l=list(l.fetchall())


print(l)

conn.close()