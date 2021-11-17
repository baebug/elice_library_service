from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from key.db_secret import flask_pw
from views import main_view, auth_view

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{flask_pw}@127.0.0.1:3306/elice_library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)  # Flask-Migrate 객체를 만들기 위해 플라스크 객체와 DB 객체 전달

from models.models import Book

app.register_blueprint(main_view.board)
app.register_blueprint(auth_view.join)

if __name__ == '__main__':
    app.run(debug=True)