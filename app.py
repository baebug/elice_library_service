from flask import Flask
from db_connect import db
from views import main_view
import config

app = Flask(__name__)
app.register_blueprint(main_view.board)

app.config.from_object(config)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)