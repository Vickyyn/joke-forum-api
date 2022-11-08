from flask import Blueprint
from init import db
from init import bcrypt
from datetime import date
from models.user import User
from models.joke import Joke
from models.tag import Tag
from models.upvote import Upvote
from models.comment import Comment
from models.joke_tag import Joke_tag


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

    jokes = [
        Joke(
            title = 'A man walked into a bar',
            body = 'and said ouch',
            date = date.today(),
            owner = 2,
            upvotes = 2
        ),
        Joke(
            title = 'What do you call a deer with no eyes?',
            body = 'no idea',
            date = date.today(),
            owner = 3,
            upvotes = 2
        ),
        Joke(
            title = 'Why was 6 afraid of 7?',
            body = 'because 7 8 9',
            date = date.today(),
            owner = 3,
            upvotes = 1
        ),
        Joke(
            title = "What is a sheep's favourite newspaper?",
            body = 'The Wool Street Journal',
            date = date.today(),
            owner = 4
        )
    ]

    db.session.add_all(jokes)
    db.session.commit()

    tags = [
        Tag(
            name = 'punny',
            description = 'things that sound like other words'
        ),
        Tag(
            name = 'bar'
        ),
        Tag(
            name = 'dad',
            description = 'funniest jokes ever'
        )
    ]

    db.session.add_all(tags)
    db.session.commit()

    upvotes = [
        Upvote(
            joke_id = 2,
            user_id = 1
        ),
        Upvote(
            joke_id = 1,
            user_id = 2
        ),
        Upvote(
            joke_id = 1,
            user_id = 3
        ),
        Upvote(
            joke_id = 3,
            user_id = 4
        ),
        Upvote(
            joke_id = 2,
            user_id = 3
        )        
    ]

    comments = [
        Comment(
            joke_id = 1,
            user_id = 1,
            date = date.today(),
            body = 'What a great joke'
        ),
        Comment(
            joke_id = 2,
            user_id = 3,
            date = date.today(),
            body = 'What do you call a fake noodle? \\n An impasta'

        ),
        Comment(
            joke_id = 2,
            user_id = 4,
            date = date.today(),
            body = 'I like deers'
        ),
        Comment(
            joke_id = 4,
            user_id = 3,
            date = date.today(),
            body = 'Baaaa'
        )
    ]

    joke_tags = [
        Joke_tag(
            joke_id = 1,
            tag_id = 2
        ),
        Joke_tag(
            joke_id = 2,
            tag_id = 1
        ),
        Joke_tag(
            joke_id = 2,
            tag_id = 3
        ),
        Joke_tag(
            joke_id = 4,
            tag_id = 3
        )
    ]

    db.session.add_all(upvotes)
    db.session.add_all(comments)
    db.session.add_all(joke_tags)
    db.session.commit()

    print('Tables seeded')

