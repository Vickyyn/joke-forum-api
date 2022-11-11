from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Allow public to register users
@auth_bp.route('/register/', methods=['POST'])
def register_users():  
    try:
        # Check validity of input (username and password constraints)
        UserSchema().load(request.json)

        user = User(
            username = request.json['username'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
        )

        db.session.add(user)
        db.session.commit() 
    
        # Respond to client and ensure valid input
        return UserSchema(exclude=['password', 'jokes', 'is_admin', 'comments']).dump(user), 201
    except IntegrityError:
        return {'error': 'Username already in use'}, 409

# Allow users to log in
@auth_bp.route('/login/', methods=['POST'])
def login_users():
    stmt = db.select(User).filter_by(username=request.json['username'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=3))
        return {'username': user.username, 'token': token}
    else:
        return {'error': 'Invalid username or password'}, 401

# Allow admin to create more admins
@auth_bp.route('/admin/', methods=['POST'])
@jwt_required()
def create_admin():
    stmt = db.select(User).filter_by(username=request.json['username'])
    new_admin = db.session.scalar(stmt)
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if new_admin and user.is_admin:
        new_admin.is_admin = True
        db.session.commit()
        return UserSchema(exclude=['password', 'jokes']).dump(new_admin)
    return {'error': 'Either user does not exist or you are not admin'}


