from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session
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
            print(valid)
            email = valid.email
            print(email)
        except EmailNotValidError as e:
            # email 틀렸음
            print(str(e))
            return jsonify({"result" : "error"})

        user = User(email, pw, name)
        print("이까지 옴1")
        db.session.add(user)
        db.session.commit()
        print("이까지 옴2")
        return jsonify({"result" : "success"})

@join.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["user_email"]
        pw = request.form["user_pw"]

        user = User.query.filter(User.user_email == email).first()

        if user:
            # 암호화된 비밀번호 검사
            if user.user_pass == pw:
                session["login"] = user.id
                return jsonify({"result" : "success"})
            else:
                return jsonify({"result" : "fail"})
        else:
            return jsonify({"result" : "fail"})

@join.route("/logout")
def logout():
    session["login"] = None
    return redirect("/")

