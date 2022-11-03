from init import db, ma

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    joke = db.relationship('Joke', back_populates='upvotes')


class UpvoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'joke_id', 'user_id')
        ordered = True


# Note this table needs to be unique