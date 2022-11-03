from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length
from models.upvote import Upvote

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
    # Display the number of upvotes for joke
    # upvotes = db.relationship('Upvote', back_populates='joke')
    # Display tags 
    joke_tags = db.relationship('Joke_tag', back_populates='joke')

class JokeSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    # Repeated maximum length for better Error display message handling
    title = fields.String(required=True, validate=Length(max=150, error='titles can only be up to 150 characters'))
    joke_tags = fields.List(fields.Nested(('Joke_tagSchema'), only=['tag_id']))
    # upvotes = fields.Function(lambda id: db.session.query(Upvote).filter(Upvote.joke_id == id).count())
    # upvotes = fields.Function(lambda id: db.session.query(Upvote).filter_by(joke_id=id).count())


    class Meta:
        fields = ('id', 'title', 'body', 'joke_tags', 'date', 'owner', 'user', 'upvotes')
        ordered = True


# list owner name rather than owner id