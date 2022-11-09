from flask import Blueprint, request
from init import db
from models.joke import Joke, JokeSchema
from models.tag import Tag, TagSchema
from models.joke_tag import Joke_tag
from models.upvote import Upvote
from models.user import User
from models.comment import Comment, CommentSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

jokes_bp = Blueprint('jokes', __name__, url_prefix='/jokes')

# Allow public to view all jokes
@jokes_bp.route('/')
def get_all_jokes():
    # Join jokes and upvotes table, then count number of times that
    # Joke.ids is repeated (this corresponds to number of upvotes)
    # Then display in descending order
    # Outerjoin to ensure jokes with 0 upvotes are also included
    stmt = db.select(Joke).outerjoin(Upvote).group_by(Joke.id).order_by(db.func.count(Joke.id).desc())
    jokes = db.session.scalars(stmt)
    return JokeSchema(many=True).dump(jokes)


# Allow users to create posts
@jokes_bp.route('/', methods=['POST'])
@jwt_required()
def create_joke():
    # Loading check to ensure input is valid
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


# Allow public to view all jokes with corresponding tag, by upvote order
# Inner join only keeps instances that exist across all 3 linked tables
@jokes_bp.route('/tags/<string:name>/')
def get_jokes_with_tag(name):
    stmt = db.select(Joke).join(Joke_tag).join(Tag).filter_by(name=name).outerjoin(Upvote).group_by(Joke.id).order_by(db.func.count(Joke.id).desc())
    jokes = db.session.scalars(stmt)
    return JokeSchema(many=True).dump(jokes)


# Allow public to view all comments
@jokes_bp.route('/comments/')
def read_all_comments():
    stmt = db.select(Comment).order_by(Comment.date.desc())
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)

# Allow users to delete their own comment, and admin to delete any comment
@jokes_bp.route('/comments/', methods=['DELETE'])
@jwt_required()
def delete_comment():
    user_id = int(get_jwt_identity())
    # Fetch user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Find comment
    stmt = db.select(Comment).filter_by(id=request.json['id'])
    comment = db.session.scalar(stmt)

    if comment:
        if comment.user_id == user_id or user.is_admin:
            db.session.delete(comment)
            db.session.commit()
            return {'message': f"Comment {request.json['id']} deleted"}
        return {'error': 'You do not have permission to do this'}, 403      
    return {'error': 'Comment not found'}, 404      



# SELECT *
# FROM jokes
# JOIN joke_tags
# ON jokes.id = joke_tags.joke_id
# JOIN tags
# ON tags.id = joke_tags.tag_id
# ;

# subq = db.select(Joke_tag).filter_by(tag_id=tag.id).subquery()
# stmt = db.select(Joke).join(subq, Joke.id == subq.c.joke_id).outerjoin(Upvote).group_by(Joke.id).order_by(db.func.count(Joke.id).desc())
# stmt = db.select(Joke).join(subq, Joke.id == subq.c.joke_id).order_by(Joke.upvotes)

# stmt = db.select(Tag).filter_by(name=name)
# tag = db.session.scalar(stmt)