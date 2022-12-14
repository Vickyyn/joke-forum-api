from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # Date of creation
    date = db.Column(db.Date) 
    body = db.Column(db.Text, nullable=False)

    user = db.relationship('User', back_populates='comments')
    joke = db.relationship('Joke', back_populates='comments')


class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    # joke = fields.Nested('JokeSchema', only=['id']) NOT needed as do not need to display the joke when viewing comments

    class Meta:
        fields = ('id', 'joke_id', 'user_id', 'date', 'body', 'user')
        ordered = True
