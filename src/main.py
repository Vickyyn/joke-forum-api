from flask import Flask
import os
from init import db, ma, bcrypt
from controllers.cli_controller import db_commands

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config ['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(db_commands)

    @app.route('/')
    def hello():
        return 'Hello World!'

    return app