from flask import Blueprint, request, abort
from init import db
from models.joke import Joke, JokeSchema
from models.upvote import Upvote, UpvoteSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from models.tag import Tag
from models.joke_tag import Joke_tag, Joke_tagSchema
from sqlalchemy.orm import joinedload, subqueryload

# Nested blueprint from jokes_bp
joke_ids_bp = Blueprint('joke_ids', __name__, url_prefix='/<int:id>')

# Check the joke ID is valid, and shows error message is not
# Used in all routes for the joke_ids_bp blueprint
def check_valid_joke(id):
    stmt = db.select(Joke).filter_by(id=id)
    joke = db.session.scalar(stmt)
    if joke:
        return joke
    else:
        abort(404, f'Joke with id {id} does not exist')

# Allow public to view specific jokes
@joke_ids_bp.route('/')
def get_one_joke(id):
    joke = check_valid_joke(id)
    return JokeSchema().dump(joke)

# Allow owner or admin to delete a joke
@joke_ids_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_one_joke(id):
    joke = check_valid_joke(id)
    user_id = int(get_jwt_identity())
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if joke.owner == user_id or user.is_admin:
        db.session.delete(joke)
        db.session.commit()
        return {'message': f'Joke {joke.id} has been deleted'}         
    else:
        return {'error': 'Jokes can only be deleted by their owner or admin'}, 403

# Allow owner to update a joke
@joke_ids_bp.route('/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_joke(id):
    joke = check_valid_joke(id)
    user_id = int(get_jwt_identity())
    if joke.owner == user_id:
        # Ensure valid update (within title character limit)
        JokeSchema().load(request.json)
        joke.title = request.json.get('title') or joke.title
        joke.body = request.json.get('body') or joke.body
        db.session.commit()
        return JokeSchema().dump(joke)
    else:
        return {'error': 'Jokes can only be edited by their owner'}, 403


# Allow users to upvote jokes
# Each user can only upvote a joke once due to validation constraint within UpvoteSchema
@joke_ids_bp.route('/upvote/', methods=['POST'])       
@jwt_required()
def upvote_joke(id):
    joke = check_valid_joke(id)
    user_id = get_jwt_identity()

    joke.upvotes = joke.upvotes + 1
    new_upvote = Upvote(
        joke_id = id,
        user_id = user_id
    )
    # Only commit if valid, error if not (will commit despite error without this line)
    UpvoteSchema().dump(new_upvote)
    db.session.add(new_upvote)
    db.session.commit()
    return UpvoteSchema().dump(new_upvote)

# Remove upvotes
@joke_ids_bp.route('/upvote/', methods=['DELETE'])       
@jwt_required()
def remove_upvote(id):
    joke = check_valid_joke(id)
    user_id = get_jwt_identity()
    # see if this particular upvote already exists
    stmt = db.select(Upvote).filter_by(joke_id=id, user_id=user_id)
    upvote = db.session.scalar(stmt)
    if upvote:
        # Decreast upvote count by 1 and delete upvote instance
        joke.upvotes = joke.upvotes - 1
        db.session.delete(upvote)
        db.session.commit()
        return {'message':f'You have removed your upvote for joke {id}'}
    return {'message': 'You have not upvoted this joke'}, 405


# Allow users or admin to add tag
@joke_ids_bp.route('/tags/', methods=['POST'])       
@jwt_required()
def add_tag(id):
    joke = check_valid_joke(id)
    user_id = int(get_jwt_identity())
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if joke.owner == user_id or user.is_admin:
        stmt = db.select(Tag).filter_by(name=request.json.get('tag'))
        tag = db.session.scalar(stmt)
        new_tag = Joke_tag(
            joke_id = id,
            tag_id = tag.id
        )
        # Ensure the new tag is valid prior to committing (if remove this line will still commit despite error)
        Joke_tagSchema().dump(new_tag)
        db.session.add(new_tag)
        db.session.commit()
        return Joke_tagSchema().dump(new_tag)



# Allow owners or admin to add tag     
# @joke_ids_bp.route('/tags/', methods=['POST'])       
# @jwt_required()
# def add_tag(id):
#     joke = check_valid_joke(id)
#     user_id = int(get_jwt_identity())
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     if joke.owner == user_id or user.is_admin:
#         # subq = db.session.query(Joke_tag).join(Joke_tag.tag).options(joinedload(Joke_tag.tag)).filter(Joke_tag.joke_id == id).filter(Tag.name == request.json.get('tags'))
#         # existing = db.session.scalar(subq)
#         # subq = db.select(Tag).where(Tag.name == request.json.get('tags')).subquery()
#         # stmt = db.select(Joke_tag).join(subq, Joke_tag.tag_id == subq.id)
#         # existing = db.session.scalars(stmt)
#         # existing = db.session.query(Joke_tag).options(subqueryload(Joke_tag.tag)).filter_by(tag == request.json.get('tags'))
#         data = request.json.get('tags')
#         stmt = db.select(Tag).filter_by(name=data)
#         tag = db.session.scalar(stmt)
#         stmts = db.select(Joke_tag).filter_by(joke_id=id, tag_id=tag.id)
#         existing = db.session.scalar(stmts)
#         if existing:
#             return {'message': 'this tag already exists'}, 405
#         elif subq:
#             new_tag_id = Joke_tag(
#                 joke_id = id,
#                 tag_id = subq.id
#             )
#             db.session.add(new_tag_id)
#             db.session.commit()
#             return Joke_tagSchema().dump(new_tag_id)
#         else:
#             new_tag = Tag(
#                 name = request.json.get('tags')
#             )
#             db.session.add(new_tag)
#             db.session.commit()

#             subq = db.select(Tag).where(Tag.name == request.json.get('tags')).subquery()

#             new_tag_id = Joke_tag(
#                 joke_id = id,
#                 tag_id = subq.id
#             )
#             db.session.add(new_tag_id)
#             db.session.commit()

#             return Joke_tagSchema().dump(new_tag_id)



# # Allow owners or admin to delete tag

# joke = check_valid_joke(id)
# user_id = get_jwt_identity()
# tag_data = request.json.get('tags')
# if tag_data:
#     for tag in tag_data:
#         entry = Tag(
#             joke_id = id,
#             user_id = user_id,

#         )




