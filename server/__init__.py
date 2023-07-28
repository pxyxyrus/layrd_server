from flask import current_app, g, Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from logger import logger

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    logger.info("Flask app created")
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
        config['database']['username'],
        config['database']['password'],
        config['database']['hostname'],
        config['database']['database']
    )
    app.app_context().push()
    db.init_app(app)
    logger.info("database connection established")

    from . import models
    # a simple page that says hello
    
    from . import user
    app.register_blueprint(user.user_bp, url_prefix='/user')
    logger.info("user api added")

    from . import project
    app.register_blueprint(project.project_bp, url_prefix='/project')
    logger.info("project api added")

    from . import application
    app.register_blueprint(application.app_bp, url_prefix='/application')
    logger.info("application api added")

    
    return app
