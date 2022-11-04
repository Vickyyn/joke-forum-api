from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


users_bp = Blueprint('users', __name__, url_prefix='/users')

# Allow public to view all users 
@users_bp.route('/')
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # Read list of users only, thus jokes each users has contributed is excluded
    # List of jokes for each user can be seen at the individual user route
    return UserSchema(many=True, exclude=['password', 'jokes']).dump(users)

# Allow public to view individual users
# View by id or by username
@users_bp.route('/<string:username>/')
@users_bp.route('/<int:id>/')
def get_one_user(username=None, id=None):
    if username:
        stmt = db.select(User).filter_by(username=username)
        user = db.session.scalar(stmt)
    elif id:
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalar(stmt)    

    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        if username:
            return {'error': f'No user found with username {username}'}, 404
        elif id:
            return {'error': f'No user found with id {id}'}, 404

# Allow users to delete their OWN account
# Allow admins to delete any account
@users_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Check user is owner, or if user is admin
        user_id = int(get_jwt_identity())
        stmt = db.select(User).filter_by(id=user_id)
        request_user = db.session.scalar(stmt)
        if id == user_id or request_user.is_admin:
            db.session.delete(user)
            db.session.commit()
            return {'message': f'Joke {id} has been deleted'}
        else:
            return {'error': 'To delete a joke you must either own it or be an admin'}, 403
    else:
        return {'error': f'No user found with id {id}'}, 404    

# Allow users to change their OWN username and/or password
# Returns resultant username, and whether password has been changed
@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_one_user(id): 
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Check user is owner; need int to avoid pass by reference
        user_id = int(get_jwt_identity())
        # Keep track if password has been changed
        password_change=False
        if id == user_id:
            # Check validity of input, and if yes assigns username if given
            UserSchema().load(request.json)
            user.username = request.json.get('username') or user.username

            # Check if password has been changed
            new_password = request.json.get('password')
            if new_password and new_password != user.password:
                user.password = new_password
                password_change=True
                db.session.commit()
            return {'message': f'Username: {user.username}; You have changed your password: {password_change}'}
        else:
            return {'error': 'You are not the user'}, 403
    else:
        return {'error': f'No user found with id {id}'}, 404   