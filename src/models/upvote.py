from init import db, ma
from marshmallow import fields, ValidationError

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Not needed: joke = db.relationship('Joke', back_populates='upvotes')


class UpvoteSchema(ma.Schema):
    # Ensure all instances are unique, that the user has not already upvoted this joke
    validation = fields.Method("is_unique_instance")
    def is_unique_instance(self, obj):
        # Count all upvotes where joke_id = joke_id of object passed in, and user_id = user_id of object passed in
        # Should be 1 if it already exists, or 0 if it does not
        stmt = db.select(db.func.count()).select_from(Upvote).filter_by(joke_id=obj.joke_id, user_id=obj.user_id)
        exist = db.session.scalar(stmt)
        if exist:
            raise ValidationError('This user has already updated this joke')

    class Meta:
        fields = ('id', 'joke_id', 'user_id', 'validation')
        ordered = True  
