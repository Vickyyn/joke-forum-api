from flask import Blueprint
from init import db
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print('Tables dropped')

