from flask import Blueprint, request, render_template, redirect, url_for, session
from flask.json import jsonify
from db_connect import db
from models.models import *

board = Blueprint('board', __name__, url_prefix='/')

@board.route("/init")
def init_data():
    book = BookCount.query.filter(BookCount.id == 1).first()
    cnt = Book.query.count()

    if not book:
        for i in range(1, cnt+1):
            a = BookCount(i, 5)
            db.session.add(a)
        db.session.commit()
    return redirect(url_for('board.book_list', page_num=1))

@board.route("/")
def index():
    return render_template("index.html")

@board.route("/page/<int:page_num>")
def book_list(page_num):
    result = Book.query.join(BookCount, Book.id == BookCount.book_id).add_columns(Book.id, Book.book_name, Book.author, Book.publisher, BookCount.cur_amount).all()
    return render_template("books_list.html", book_list = result, page_num = page_num)

@board.route("/book/<int:book_id>", methods=["GET", "POST"])
def book_detail(book_id):
    if request.method == "GET":
        book = Book.query.filter(Book.id == book_id).first()
        review_list = Review.query.filter(Review.book_id == book_id).all()
        return render_template("book_detail.html", book = book, review_list=review_list)
    elif request.method == "POST":
        user_id = session.get("login")
        grade = request.form["star"]
        desc = request.form["review"]

        review = Review(book_id, user_id, desc, grade)
        db.session.add(review)
        db.session.commit()
        return jsonify({"result": "success"})