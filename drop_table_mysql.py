import pymysql
from key.db_secret import flask_pw

db_connection = pymysql.connect(
    user    = 'root',
    passwd  = flask_pw,
    host    = '127.0.0.1',
    db      = 'elice_library',
    charset = 'utf8'
    )
    
con = db_connection
cur = con.cursor(pymysql.cursors.DictCursor)
cur.execute("DROP TABLE reviews;")
cur.execute("DROP TABLE borrow;")
cur.execute("DROP TABLE users;")
cur.execute("DROP TABLE books_amount;")
cur.execute("DROP TABLE books;")
cur.execute("DROP TABLE alembic_version;")
con.commit()
con.close()