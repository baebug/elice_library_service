import sqlite3
import csv

con = sqlite3.connect("./db.sqlite3") # 빈 .db파일 생성
cur = con.cursor()
cur.execute("create table books (id integer primary key autoincrement, book_name text, publisher text, author text, publication_date DATETIME, pages integer, isbn integer, description text, link text);")

# csv 파일 읽기
# 인코딩 문제 나오면 encoding = ''에 utf-8 > euc-kr > cp949 순서로 해봐라
with open('book_list.csv') as datas :
    records = csv.DictReader(datas)
    result = [ (w['book_name'], w['publisher'], w['author'], w['publication_date'], w['pages'], w['isbn'], w['description'], w['link']) for w in records]

# csv 파일 sqlite3 디비에 삽입
cur.executemany("insert into books(book_name, publisher, author, publication_date, pages, isbn, description, link) values(?, ?, ?, ?, ?, ?, ?, ?);", result)

con.commit()
con.close()