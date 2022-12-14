from flask import Blueprint, request, abort
from init import db
from models.joke import Joke, JokeSchema
from models.upvote import Upvote, UpvoteSchema
from models.comment import Comment, CommentSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from models.tag import Tag
from models.joke_tag import Joke_tag, Joke_tagSchema
from datetime import date

# Nested blueprint from jokes_bp
joke_ids_bp = Blueprint('joke_ids', __name__, url_prefix='/<int:id>')

# Check the joke ID is valid, and shows error message if not
# Used in all routes for the joke_ids_bp blueprint
def check_valid_joke(id):
    # Get joke with id of the argument passed in
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
    # Get requesting user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Check if requesting user is the creator of the joke, or if they are admin
    if joke.owner == user_id or user.is_admin:
        # Delete joke from database and commit/save changes
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
        # Commit/save changes to database
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

    new_upvote = Upvote(
        joke_id = id,
        user_id = user_id
    )
    # Only commit if valid, error if not (will commit despite error without this line)
    UpvoteSchema().dump(new_upvote)
    # Add and commit/save the new upvote to the database
    db.session.add(new_upvote)
    db.session.commit()
    return UpvoteSchema(exclude=['validation']).dump(new_upvote), 201

# Allow users to remove their own upvotes
@joke_ids_bp.route('/upvote/', methods=['DELETE'])       
@jwt_required()
def remove_upvote(id):
    joke = check_valid_joke(id)
    user_id = get_jwt_identity()
    # Get the upvote where joke_id = id of joke (argument passed in) and user_id = requesting user
    # To see if this particular upvote already exists
    stmt = db.select(Upvote).filter_by(joke_id=id, user_id=user_id)
    upvote = db.session.scalar(stmt)
    if upvote:
        # Delete upvote instance and commit/save changes to database
        db.session.delete(upvote)
        db.session.commit()
        return {'message':f'You have removed your upvote for joke {id}'}
    return {'message': 'There is no associated upvote for you to delete'}, 405


# Allow owners or admin to add tag to a joke
@joke_ids_bp.route('/tags/', methods=['POST'])       
@jwt_required()
def add_tag(id):
    joke = check_valid_joke(id)
    user_id = int(get_jwt_identity())
    # Get requesting user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Check if requesting user is the owner of the joke, or if they are admin
    if joke.owner == user_id or user.is_admin:
        data = request.json.get('tag')
        if not data:
            raise ValidationError('Please input a tag')
        # Get tag that matches the input name/data
        stmt = db.session.query(Tag).filter_by(name=data)
        tag = db.session.scalar(stmt)
        # If tag does not already exist, create a new tag instance
        if not tag:
            new_tag = Tag(
                name = data
            )
            db.session.add(new_tag)
            db.session.commit()
        
            # retrieve tag that was just created
            stmt = db.session.query(Tag).filter_by(name=data)
            tag = db.session.scalar(stmt)

        new_joke_tag = Joke_tag(
            joke_id = id,
            tag_id = tag.id
        )
        # Ensure valid unique joke tag prior to committing; error if not
        # i.e. that it does not already exist, validation check within joke_tag schema
        Joke_tagSchema().dump(new_joke_tag)
        db.session.add(new_joke_tag)
        db.session.commit()
        return Joke_tagSchema(exclude=['validation']).dump(new_joke_tag), 201
    return {'error': 'You do not have permission to do this'}, 403


# Allow owners or admin to delete tags
@joke_ids_bp.route('/tags/', methods=['DELETE'])       
@jwt_required()
def delete_tag(id):
    joke = check_valid_joke(id)
    user_id = int(get_jwt_identity())
    # Get requesting user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Check if requesting user is owner of joke, or if they are admin
    if joke.owner == user_id or user.is_admin:
        # Select the corresponding joke tag instance: 
        # Get tags where the name correspond to the requesting tag name
        # Then get joke_tags where the tag_id is the same as the ids of the tags from above
        # Then filter to only include joke_tags where the joke_id = id of the joke
        subq = db.select(Tag).filter_by(name=request.json['tag']).subquery()
        stmt = db.select(Joke_tag).join(subq, Joke_tag.tag_id == subq.c.id).filter(Joke_tag.joke_id==id)
        tag = db.session.scalar(stmt)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return {"message": f"you have deleted the tag {request.json.get('tag')} from joke {id}"}
        raise ValidationError('This tag did not exist')
    raise ValidationError('You do not have permission to do this')

# Allow public to view comments for specific joke
@joke_ids_bp.route('/comments/')
def see_comments_for_joke(id):
    joke = check_valid_joke(id)
    # Get all comments for a specific joke (get all comments and filter by joke_id = id of joke)
    stmt = db.select(Comment).filter_by(joke_id=id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)

# Allow users to add a comment
@joke_ids_bp.route('/comments/', methods=['POST'])
@jwt_required()
def add_comment(id):
    joke = check_valid_joke(id)
    user_id = get_jwt_identity()
    if len(request.json['body']) == 0:
        raise ValidationError('Comments cannot be empty')
    comment = Comment(
        joke_id = id,
        user_id = user_id,
        body = request.json['body'],
        date = date.today()
    )
    # Add and commit/save comment to database
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201

# Note comment deletion is in the jokes controller