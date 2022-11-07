from init import db, ma
from marshmallow import validates
from marshmallow.exceptions import ValidationError
from marshmallow import fields


class Joke_tag(db.Model):
    __tablename__ = 'joke_tags'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

    joke = db.relationship('Joke', back_populates='joke_tags')
    tag = db.relationship('Tag', back_populates='joke_tags')

class Joke_tagSchema(ma.Schema):
    tag = fields.Nested('TagSchema', only=['name'])

    class Meta:
        fields = ('id', 'joke_id', 'tag_id', 'tag')
        ordered = True

# joke_tag = Table(
#     "joke_tags",
#     db.Base.metadata,
#     db.Column('joke_id', db.ForeignKey('jokes.id'), primary_key=True),
#     db.Column('tag_id', db.ForeighKey('tags.id'), primary_key=True)
# ) 



# Note this table needs to be unique