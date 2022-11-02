from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    jokes = db.relationship('Joke', back_populates='user', cascade=False)


class UserSchema(ma.Schema):
    jokes = fields.List(fields.Nested('JokeSchema', exclude=['user', 'owner']))

    class Meta:
        fields = ('id', 'username', 'password', 'jokes')
        ordered = True

# username need minimum length 4
# password minimum length 4
