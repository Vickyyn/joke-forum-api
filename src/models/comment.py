from init import db, ma

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # Date of creation
    date = db.Column(db.Date) 
    body = db.Column(db.Text, nullable=False)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'joke_id', 'user_id', 'date', 'body')
        ordered = True
