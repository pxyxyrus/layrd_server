import flask
from flask_sqlalchemy import SQLAlchemy


app = flask.current_app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
db = SQLAlchemy(app)








def create_user():
    pass


