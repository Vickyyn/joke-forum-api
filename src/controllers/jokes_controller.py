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

# # Allow public to view all jokes with corresponding tag
@jokes_bp.route('/tags/<string:name>/')
def get_jokes_with_tag(name):
    # Retrieve id of tag from name
    # stmt = db.select(Tag).filter_by(name=name)
    # tag = db.session.scalar(stmt)
    # # Retrieve all joke ids with corresponding tag id
    # stmt = db.select(Joke_tag).filter_by(tag_id=tag.id)
    # x = db.session.scalars(stmt)

    # # Convert corresponding values into a list
    # joke_ids = Joke_tagSchema(many=True).dump(x)
    # valid_ids = [entry['joke_id'] for entry in joke_ids]


    # # Retrieve all jokes with ids in the list
    # # for i in valid_ids:
    # #     stmt = db.select(Joke).filter_by(id=i)
    # # stmt = db.select(Joke).filter_by(id==[i for i in valid_ids])
    # # jokes = db.session.scalars(stmt)

    # x = JokeSchema(many=True).dump(jokes_ids)
    # # Retrieve all jokes from joke ids
    # stmt = db.select(Joke).filter_by(id=x.joke_id)
    # jokes = db.session.scalars(stmt)

    # tag = db.session.query(Tag).filter(name=name)
    

    # return JokeSchema(many=True).dump(jokes)


    stmt = db.select(Tag).filter_by(name=name)
    tag = db.session.scalar(stmt)

    # Retrieve all joke ids with corresponding tag id
    stmt = db.select(Joke_tag).filter_by(tag_id=tag.id)
    x = db.session.scalars(stmt)

    # Convert corresponding values into a list
    joke_ids = Joke_tagSchema(many=True).dump(x)
    valid_ids = [entry['joke_id'] for entry in joke_ids]
    print(valid_ids)
    # Retrieve all jokes with ids in the list

    stmt = db.select(Joke).filter(Joke.id in [1]) # NOT WORKING HERE
    jokes = db.session.scalars(stmt)
    jokes = []
    for id in valid_ids:
        xy = db.select(Joke).where(Joke.id == id)
        jokes.append(db.session.scalar(xy))

    return JokeSchema(many=True).dump(jokes)

