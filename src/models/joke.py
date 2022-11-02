from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class Joke(db.Model):
    __tablename__ = 'jokes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # Date of creation
    date = db.Column(db.Date) 
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    # Display the username as well as the owner(user_id)
    user = db.relationship('User', back_populates='jokes')

class JokeSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    title = fields.String(required=True, validate=Length(max=150, error='titles can only be up to 150 characters'))

    class Meta:
        fields = ('id', 'title', 'body', 'date', 'owner', 'user')
        ordered = True


# list owner name rather than owner id