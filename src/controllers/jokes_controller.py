from flask import Blueprint
from init import db
from models.joke import Joke, JokeSchema


jokes_bp = Blueprint('jokes', __name__, url_prefix='/jokes')

@jokes_bp.route('/')
def get_all_jokes():
    stmt = db.select(Joke)
    jokes = db.session.scalars(stmt)
    return JokeSchema(many=True).dump(jokes)


@jokes_bp.route('/<int:id>/')
def get_one_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        return JokeSchema().dump(joke)
    else:
        return {'error': f'No joke found with id {id}'}, 404

@jokes_bp.route('/<int:id>/', methods=['DELETE'])
def delete_one_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        db.session.delete(joke)
        db.session.commit()
        return {'message': f'Joke {joke.id} has been deleted'}
    else:
        return {'error': f'No joke found with id {id}'}, 404