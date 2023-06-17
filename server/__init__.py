import os

from flask import Flask

app = Flask(__name__)


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import authenticate
    app.register_blueprint(authenticate.auth_bp)

    
    return app
