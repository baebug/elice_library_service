from db_connect import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=False)

class BookCount(db.Model):
    __tablename__ = 'books_amount'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    cur_amount = db.Column(db.Integer, nullable=False)

    def __init__(self, book_id, amount):
        self.book_id = book_id
        self.total_amount = amount
        self.cur_amount = amount

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(30), nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(30), nullable=False)

    def __init__(self, email, password, name):
        self.user_email = email
        self.user_pass = password
        self.user_name = name

class Borrow(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    borrowed = db.Column(db.Boolean, default=True)

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    def __init__(self, book_id, user_id, desc, grade):
        self.book_id = book_id
        self.user_id = user_id
        self.description = desc
        self.grade = grade