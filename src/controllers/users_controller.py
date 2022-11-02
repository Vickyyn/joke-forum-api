from flask import Blueprint
from init import db
from models.user import User, UserSchema


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # Read list of users only, thus jokes each users has contributed is excluded
    # List of jokes for each user can be seen at the individual user route
    return UserSchema(many=True, exclude=['password', 'jokes']).dump(users)

@users_bp.route('/<string:username>/')
def get_one_user(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        return {'error': f'No user found with username {id}'}, 404    

@users_bp.route('/<string:username>/', methods=['DELETE'])
def delete_one_user(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.username} has been deleted'}
    else:
        return {'error': f'No user found with username {username}'}, 404    

