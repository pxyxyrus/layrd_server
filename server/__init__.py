from flask import current_app, g, Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
        config['database']['username'],
        config['database']['password'],
        config['database']['hostname'],
        config['database']['database']
    )
    app.app_context().push()
    db.init_app(app)

    from . import models

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import authenticate
    app.register_blueprint(authenticate.auth_bp)

    from . import project
    app.register_blueprint(project.project_bp)

    
    return app
