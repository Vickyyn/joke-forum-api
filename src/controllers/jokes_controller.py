from flask import Blueprint, request
from init import db
from models.joke import Joke, JokeSchema
from models.tag import Tag, TagSchema
from models.joke_tag import Joke_tag, Joke_tagSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

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

# Allow users to create posts
@jokes_bp.route('/', methods=['POST'])
@jwt_required()
def create_joke():
    data = JokeSchema().load(request.json)
    joke = Joke(
        title = data['title'],
        body = data['body'],
        date = date.today(),
        owner = get_jwt_identity()
    )
    db.session.add(joke)
    db.session.commit()
    return JokeSchema().dump(joke), 201

# Allow public to view all tags
@jokes_bp.route('/tags/')
def get_all_tags():
    stmt = db.select(Tag)
    tags = db.session.scalars(stmt)
    return TagSchema(many=True).dump(tags)

# Allow users to add tags
@jokes_bp.route('/tags/', methods=['POST'])
    tag_name = request.json['name']



# # Allow public to view all jokes with corresponding tag
@jokes_bp.route('/tags/<string:name>/')
def get_jokes_with_tag(name):
    stmt = db.select(Tag).filter_by(name=name)
    tag = db.session.scalar(stmt)

    # joke = db.select(Joke_tag.joke).filter_by(tag_id=tag.id)
    # jokes = db.session.scalars(joke)
    

    # jokes = (
    #     db.session.query(Joke).join(Joke.joke_tags).filter(Joke_tag.tag_id == tag.id).order_by(Joke.upvotes).all()
    # )
    # db.session.scalars(jokes)

    subq = db.select(Joke_tag).filter_by(tag_id=tag.id).subquery()
    stmt = db.select(Joke).join(subq, Joke.id == subq.c.joke_id).order_by(Joke.upvotes)
    jokes = db.session.scalars(stmt)

    # jokes = db.select(Joke).join(Joke.joke_tags).join(Joke_tag.tag).where(Tag.name == name)
    # stmt = db.session.scalars(jokes)

    # # Retrieve all joke ids with corresponding tag id
    # stmt = db.select(Joke_tag).filter_by(tag_id=tag.id)
    # x = db.session.scalars(stmt)

    # # Convert corresponding values into a list
    # joke_ids = Joke_tagSchema(many=True).dump(x)
    # valid_ids = [entry['joke_id'] for entry in joke_ids]

    # # Retrieve all jokes with ids in the list
    # jokes = []
    # for id in valid_ids:
    #     joke = db.select(Joke).where(Joke.id == id)
    #     jokes.append(db.session.scalar(joke))

    return JokeSchema(many=True).dump(jokes)
