from flask import Blueprint, request, render_template, redirect, url_for, session
from flask.json import jsonify
from db_connect import db
from models.models import *
from datetime import datetime
from sqlalchemy import func

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
    avg_grade_list = db.session.query(Review, func.avg(Review.grade)).group_by(Review.book_id).all()
    return render_template("books_list.html", book_list = result, page_num = page_num, avg_grade_list=avg_grade_list)

@board.route("/book/<int:book_id>", methods=["GET"])
def book_detail(book_id):
    if request.method == "GET":
        user_id = session.get("login")

        book = Book.query.join(BookCount, Book.id == BookCount.book_id).add_columns(Book.id, Book.book_name, Book.author, Book.publisher, Book.publication_date, Book.pages, Book.isbn, Book.description, Book.link, BookCount.cur_amount).filter(Book.id == book_id).first()
        avg_grade = db.session.query(Review, func.avg(Review.grade)).filter(Review.book_id == book_id).first()
        review_list = Review.query.join(User, Review.user_id == User.id).add_columns(Review.id, Review.user_id, Review.book_id, Review.grade, Review.description, Review.review_date, User.user_name).filter(Review.book_id == book_id).order_by(Review.review_date.desc()).all()
        _isBorrow = Borrow.query.filter((Borrow.user_id == user_id), (Borrow.book_id == book_id), (Borrow.borrowed == 1)).first()
        if _isBorrow:
            isBorrow = True
        else:
            isBorrow = False
        
        return render_template("book_detail.html", book = book, review_list=review_list, isBorrow=isBorrow, avg_grade=avg_grade)
    

@board.route("/book/<int:book_id>/review", methods=["POST", "DELETE"])
def review(book_id):
    if request.method == "POST":
        user_id = session.get("login")
        grade = request.form["star"]
        desc = request.form["review"]

        review = Review(book_id, user_id, desc, grade)
        db.session.add(review)
        db.session.commit()
        return jsonify({"result": "success"})
    elif request.method == "DELETE":
        review_id = request.form["review_id"]

        review = Review.query.filter(Review.id == review_id).first()
        db.session.delete(review)
        db.session.commit()
        return jsonify({"result": "success"})

@board.route("/book/<int:book_id>/borrow", methods=["POST"])
def borrow(book_id):
    if request.method == "POST":
        user_id = session.get("login")

        book = BookCount.query.filter(BookCount.book_id == book_id).first()
        book.cur_amount -= 1

        borrow = Borrow(book_id, user_id)
        db.session.add(borrow)
        db.session.commit()
        return jsonify({"result": "success"})

@board.route("/book/<int:book_id>/return", methods=["POST"])
def returnBook(book_id):
    if request.method == "POST":
        user_id = session.get("login")

        book = BookCount.query.filter(BookCount.book_id == book_id).first()
        book.cur_amount += 1

        borrow = Borrow.query.filter((Borrow.user_id == user_id), (Borrow.book_id == book_id), (Borrow.borrowed == 1)).first()
        borrow.return_date = datetime.utcnow()
        borrow.borrowed = 0
        db.session.commit()
        return jsonify({"result": "success"})

@board.route("/borrow", methods=["GET"])
def borrowList():
    if request.method == "GET":
        user_id = session.get("login")

        borrow_list = Borrow.query.join(Book, Book.id == Borrow.book_id).add_columns(Book.id, Book.book_name, Borrow.borrow_date, Borrow.return_date, Borrow.borrowed).filter(Borrow.user_id == user_id).all()

        return render_template("borrow_list.html", borrow_list=borrow_list)

@board.route("/test")
def test():
    list = db.session.query(Review, func.avg(Review.grade)).group_by(Review.book_id).all()
    return render_template("test.html", list=list)