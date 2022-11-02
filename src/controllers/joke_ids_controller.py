from flask import Blueprint, request
from init import db
from models.joke import Joke, JokeSchema

# Nested blueprint from jokes_bp
joke_ids_bp = Blueprint('joke_ids', __name__, url_prefix='/<int:id>')

# Allow public to view specific jokes
@joke_ids_bp.route('/')
def get_one_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        return JokeSchema().dump(joke)
    else:
        return {'error': f'No joke found with id {id}'}, 404

# Allow owner or admin to delete a joke
@joke_ids_bp.route('/', methods=['DELETE'])
def delete_one_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        db.session.delete(joke)
        db.session.commit()
        return {'message': f'Joke {joke.id} has been deleted'}
    else:
        return {'error': f'No joke found with id {id}'}, 404

# Allow owner to update a joke
@joke_ids_bp.route('/', methods=['PUT', 'PATCH'])
def update_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        # Ensure valid update (within title character limit)
        JokeSchema().load(request.json)
        joke.title = request.json.get('title') or joke.title
        joke.body = request.json.get('body') or joke.body
        db.session.commit()
        return JokeSchema().dump(joke)
    else:
        return {'error': f'No joke found with id {id}'}, 404        