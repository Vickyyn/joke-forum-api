from flask import Flask
import os
from init import db, ma, bcrypt
from controllers.cli_controller import db_commands
from controllers.jokes_controller import jokes_bp
from controllers.users_controller import users_bp
from marshmallow.exceptions import ValidationError

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config ['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(jokes_bp)
    app.register_blueprint(users_bp)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 404

    @app.route('/')
    def hello():
        return 'Welcome to the jokes forum!'

    return app