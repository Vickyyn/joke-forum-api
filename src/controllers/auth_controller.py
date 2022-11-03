from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError


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
        return UserSchema(exclude=['password', 'jokes']).dump(user), 201
    except IntegrityError:
        return {'error': 'Username already in use'}, 409

@auth_bp.routeh('/login/', methods=['POST'])
def login_users():
