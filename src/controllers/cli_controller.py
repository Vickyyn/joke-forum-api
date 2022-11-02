from flask import Blueprint
from init import db
from models.user import User
from models.joke import Joke
from models.upvote import Upvote
from init import bcrypt

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            username = 'admin',
            password = bcrypt.generate_password_hash('admins').decode('utf-8'),
            is_admin = True
        ),
        User(
            username = 'Charlie',
            password = bcrypt.generate_password_hash('angels').decode('utf-8'),
        ),
        User(
            username = 'Alice',
            password = bcrypt.generate_password_hash('wonderland').decode('utf-8'),
        ),
        User(
            username = 'Rhys',
            password = bcrypt.generate_password_hash('wales').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    # jokes = [
    #     Joke(
    #         title = 'A man walked into a bar'

    #     )
    # ]