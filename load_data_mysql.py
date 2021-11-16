import pymysql
import csv
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
cur.execute("CREATE TABLE books (id integer primary key auto_increment, book_name varchar(50), publisher varchar(30), author varchar(30), publication_date DATETIME, pages integer, isbn bigint(20), description text, link varchar(256));")

with open('book_list.csv') as datas :
    records = csv.DictReader(datas)
    result = [ (w['book_name'], w['publisher'], w['author'], w['publication_date'], w['pages'], w['isbn'], w['description'], w['link']) for w in records]

# csv 파일 sqlite3 디비에 삽입
cur.executemany("insert into books(book_name, publisher, author, publication_date, pages, isbn, description, link) values(%s, %s, %s, %s, %s, %s, %s, %s);", result)

con.commit()
con.close()