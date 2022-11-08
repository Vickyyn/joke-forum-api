from init import db, ma
from marshmallow import validates, fields, ValidationError

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # joke = db.relationship('Joke', back_populates='upvotes')


class UpvoteSchema(ma.Schema):
    # Ensure all instances are unique
    validation = fields.Method("is_unique_instance")
    
    def is_unique_instance(self, obj):
        stmt = db.select(db.func.count()).select_from(Upvote).filter_by(joke_id=obj.joke_id, user_id=obj.user_id)
        exist = db.session.scalar(stmt)
        if exist > 1:
            raise ValidationError('This particular instance already exists')

    class Meta:
        fields = ('id', 'joke_id', 'user_id', 'validation')
        ordered = True  


# Note this table needs to be unique