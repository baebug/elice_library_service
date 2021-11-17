from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from db_connect import db
from models.models import *

from email_validator import validate_email, EmailNotValidError

join = Blueprint('join', __name__, url_prefix='/')


@join.route("/regist", methods=["GET", "POST"])
def regist():
    if request.method == "GET":
        return render_template("regist.html")
    elif request.method == "POST":
        email = request.form["user_email"]
        pw = request.form["user_pw"]
        name = request.form["user_name"]
        # 각종 예외처리
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            # email 틀렸음
            print(str(e))

        user = User(email, pw, name)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result" : "success"})