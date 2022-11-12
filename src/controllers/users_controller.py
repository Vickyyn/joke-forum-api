from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


users_bp = Blueprint('users', __name__, url_prefix='/users')

# Allow public to view all users 
@users_bp.route('/')
def get_all_users():
    # Get all users
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # Read list of users only, thus jokes each users has contributed is excluded
    # List of jokes for each user can be seen at the individual user route
    return UserSchema(many=True, exclude=['password', 'jokes']).dump(users)

# Allow public to view individual users
# View by id or by username
# Note username cannot be only numbers so there will be no overlap
@users_bp.route('/<string:username>/')
@users_bp.route('/<int:id>/')
def get_one_user(username=None, id=None):
    if username:
        # Get user where username = username passed in (get selected user)
        stmt = db.select(User).filter_by(username=username)
        user = db.session.scalar(stmt)
    elif id:
        # Get user where id = id passed in (get selected user)
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
    # Get user where id = id passed in (get the user selected)
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Check if requesting user corresponds to the user selected, or if requesting user is admin
        # Need int to avoid pass by reference
        user_id = int(get_jwt_identity())
        # Get user where id = user_id of the requesting user (get the requesting user)
        stmt = db.select(User).filter_by(id=user_id)
        request_user = db.session.scalar(stmt)
        if id == user_id or request_user.is_admin:
            # Delete selected user
            db.session.delete(user)
            db.session.commit()
            return {'message': f'User {id} has been deleted'}
        else:
            return {'error': 'To delete a user you must either be the user or be an admin'}, 403
    else:
        return {'error': f'No user found with id {id}'}, 404    

# Allow users to change their password
@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_password(id): 
    # Get user where id = id passed in (get selected user)
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Check requesting user is the same as selected user; need int to avoid pass by reference
        user_id = int(get_jwt_identity())
        # Check the requesting user matches the selected user, and that the old password provided is correct
        if (id == user_id) and bcrypt.check_password_hash(user.password, request.json['old_password']):
            # Ensure valid passwords
            if len(request.json['new_password']) < 4:
                return {'error': 'Passwords must be at lesat 4 characters long'}, 400
            user.password = bcrypt.generate_password_hash(request.json['new_password']).decode('utf-8')
            # Save/commit changes applied
            db.session.commit()
            return {'message': 'You have changed your password'}
        return {'error': 'You are not the user, or the password is incorrect'}, 403 
    return {'error': f'No user found with id {id}'}, 404   