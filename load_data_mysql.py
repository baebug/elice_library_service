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

with open('book_list.csv') as datas :
    records = csv.DictReader(datas)
    result = [ (w['book_name'], w['publisher'], w['author'], w['publication_date'], w['pages'], w['isbn'], w['description'], w['link']) for w in records]

cur.executemany("insert into books(book_name, publisher, author, publication_date, pages, isbn, description, link) values(%s, %s, %s, %s, %s, %s, %s, %s);", result)
con.commit()
con.close()

# cur.execute("CREATE TABLE books (id integer primary key auto_increment, book_name varchar(50), publisher varchar(30), author varchar(30), publication_date DATETIME, pages integer, isbn varchar(15), description text, link varchar(255));")
# cur.execute("CREATE TABLE books_amount (id integer primary key auto_increment, book_id integer, total_amount integer, cur_amount integer, FOREIGN KEY (book_id) REFERENCES books (id));")
# cur.execute("CREATE TABLE users (id integer primary key auto_increment, user_email varchar(30), user_pass varchar(255), user_name varchar(30));")
# cur.execute("CREATE TABLE borrow (id integer primary key auto_increment, book_id integer, user_id integer, borrow_date DATETIME, return_date DATETIME, borrowed boolean default 1, FOREIGN KEY (book_id) REFERENCES books (id), FOREIGN KEY (user_id) REFERENCES users (id));")
# cur.execute("CREATE TABLE reviews (id integer primary key auto_increment, book_id integer, user_id integer, description text, grade integer, FOREIGN KEY (book_id) REFERENCES books (id), FOREIGN KEY (user_id) REFERENCES users (id));")
