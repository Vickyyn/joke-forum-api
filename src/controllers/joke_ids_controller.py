from flask import Blueprint, request
from init import db
from models.joke import Joke, JokeSchema
from models.upvote import Upvote
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

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
@jwt_required()
def delete_one_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        # Ensure only owner or admin can delete
        # int to avoid pass by reference
        user_id = int(get_jwt_identity())
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if joke.owner == user_id or user.is_admin:
            db.session.delete(joke)
            db.session.commit()
            return {'message': f'Joke {joke.id} has been deleted'}         
        else:
            raise ValidationError('Jokes can only be deleted by their owner or admin')
    else:
        return {'error': f'No joke found with id {id}'}, 404

# Allow owner to update a joke
@joke_ids_bp.route('/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_joke(id):
    # Ensure joke exists and retrieve joke
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        # Ensure only owner can update
        # int to avoid pass by reference (will not work otherwise)
        user_id = int(get_jwt_identity())
        if joke.owner == user_id:
            # Ensure valid update (within title character limit)
            JokeSchema().load(request.json)
            joke.title = request.json.get('title') or joke.title
            joke.body = request.json.get('body') or joke.body
            db.session.commit()
            return JokeSchema().dump(joke)
        else:
            raise ValidationError('Jokes can only be edited by their owner')
    else:
        return {'error': f'No joke found with id {id}'}, 404 

# Allow users to upvote jokes
# Each user can only upvote a joke once
# Users can also remove their upvotes
@joke_ids_bp.route('/upvote/', methods=['POST'])       
@jwt_required()
def upvote_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:    
        user_id = get_jwt_identity()
        # see if this particular upvote already exists
        stmt = db.select(Upvote).filter_by(joke_id=id, user_id=user_id)
        upvote = db.session.scalar(stmt)
        if request.json.get('upvote') == 'yes':
            if upvote:
                # response 405 is method not allowed
                return {'message': 'You cannot upvote the same joke twice'}, 405
            else:
                # Increase upvote count by 1 and create new upvote instance
                joke.upvotes = joke.upvotes + 1
                new_upvote = Upvote(
                    joke_id = id,
                    user_id = user_id
                )
                db.session.add(new_upvote)
                db.session.commit()
                return {'message': f'You have upvoted joke {id}'}
        elif request.json.get('upvote') == 'no':
            if upvote:
                # Decreast upvote count by 1 and delete upvote instance
                joke.upvotes = joke.upvotes - 1
                db.session.delete(upvote)
                db.session.commit()
                return {'message':f'You have removed your upvote for joke {id}'}
            else:
                return {'message': 'You have not upvoted this joke'}, 405
        else:
            return {'error': "You must input 'upvote' as 'yes' or 'no'"}, 400
        

