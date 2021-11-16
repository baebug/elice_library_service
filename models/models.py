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
    isbn = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(256), nullable=False)
