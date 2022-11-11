from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    jokes = db.relationship('Joke', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')


class UserSchema(ma.Schema):
    jokes = fields.List(fields.Nested('JokeSchema', exclude=['user', 'owner']))
    username = fields.String(required=True, validate=And(
        Length(min=4, max=20, error='username must be between 4 - 20 characters long'),
        Regexp('(?!^\d+$)^.+$', error = 'You cannot have a username with only numbers'),
        Regexp('^[a-zA-Z0-9]+$', error='Only numbers and letters are allowed')
    ))
    password = fields.String(required=True, validate=Length(min=4, error='password must be at least 4 characters long'))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))


    class Meta:
        fields = ('id', 'username', 'password', 'jokes', 'is_admin', 'comments')
        ordered = True