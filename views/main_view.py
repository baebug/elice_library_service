from flask import Blueprint, request, render_template
from db_connect import db
from models.models import Book

board = Blueprint('board', __name__, url_prefix='/')

@board.route("/")
def index():
    result = Book.query.all()
    return render_template("index.html", book_list = result)