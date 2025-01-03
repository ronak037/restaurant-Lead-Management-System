import os

class DBConfig(object):
    DB_USERNAME=os.environ.get("DB_USERNAME")
    DB_PASSWORD=os.environ.get("DB_PASSWORD")
    DB_PORT=os.environ.get("DB_PORT")
    DB_NAME=os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
