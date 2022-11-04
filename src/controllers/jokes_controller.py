from flask import Blueprint, request
from init import db
from models.joke import Joke, JokeSchema
from models.tag import Tag, TagSchema
from models.joke_tag import Joke_tag

jokes_bp = Blueprint('jokes', __name__, url_prefix='/jokes')

# Allow public to view all jokes
@jokes_bp.route('/')
def get_all_jokes():
    # stmt = db.select(Joke).order_by(db.session.query(Joke_tag).filter(Joke_tag.joke_id==Joke.id).count())
    stmt = db.select(Joke).order_by(Joke.upvotes.desc())
    jokes = db.session.scalars(stmt)
    # jokes.order_by(
    #     db.session.query(Joke_tag).filter_by(Joke_tag.joke_id==Joke.id).count()
    # )
    # db.session.query(Upvote).filter_by(joke_id=obj.id).count()
    return JokeSchema(many=True).dump(jokes)

# Allow public to view all tags
@jokes_bp.route('/tags/')
def get_all_tags():
    stmt = db.select(Tag)
    tags = db.session.scalars(stmt)
    return TagSchema(many=True).dump(tags)

# Allow public to view all jokes with corresponding tag
# @jokes_bp.route('/tags/<string:name>/')
# def get_jokes_with_tag(name):
#     # Retrieve id of tag from name
#     stmt = db.select(Tag).filter_by(name=name)
#     tag = db.session.scalar(stmt)
#     # Retrieve all joke ids with corresponding tag id
#     stmt = db.select(Joke_tag).filter_by(tag_id=tag.id)
#     joke_ids = db.session.scalars(stmt)
#     # Retrieve all jokes from joke ids
#     stmt = db.select(Joke).filter_by(id.in_(joke_ids.joke_id))
#     jokes = db.session.scalars(stmt)

#     return JokeSchema(many=True).dump(jokes)

