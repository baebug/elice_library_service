from key.db_secret import flask_pw

db = {
    'user': 'root',
    'password': flask_pw,
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'elice_library'
}

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False