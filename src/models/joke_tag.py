from init import db, ma

class Joke_tag(db.Model):
    __tablename__ = 'joke_tags'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)


class Joke_tagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'joke_id', 'tag_id')
        ordered = True


# Note this table needs to be unique