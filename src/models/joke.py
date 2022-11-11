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
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Display the username as well as the owner(user_id)
    user = db.relationship('User', back_populates='jokes')
    joke_tags = db.relationship('Joke_tag', back_populates='joke', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='joke', cascade='all, delete')


class JokeSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    # Repeated maximum length for better Error display message handling
    title = fields.String(required=True, validate=Length(max=150, error='titles can only be up to 150 characters'))
    joke_tags = fields.List(fields.Nested(('Joke_tagSchema'), only=['tag']))
    # Include upvotes in display of jokes, calculated from database
    upvotes = fields.Function(lambda obj: db.session.query(Upvote).filter_by(joke_id=obj.id).count())
    comments = fields.List(fields.Nested('CommentSchema', exclude=['joke_id']))

    class Meta:
        fields = ('id', 'title', 'body', 'joke_tags', 'date', 'owner', 'user', 'upvotes', 'comments')
        ordered = True


# list owner name rather than owner id
# SELECT joke_id, count(joke_id)                                                                      
# FROM jokes LEFT JOIN upvotes
# ON jokes.id = upvotes.joke_id
# GROUP BY joke_id;