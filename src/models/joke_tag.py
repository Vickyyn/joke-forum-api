from init import db, ma
from marshmallow import validates
from marshmallow.exceptions import ValidationError

class Joke_tag(db.Model):
    __tablename__ = 'joke_tags'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

    joke = db.relationship('Joke', back_populates='joke_tags')

class Joke_tagSchema(ma.Schema):

    # @validates('joke_id')
    # def validate_tag(self, name, description):
    #     if name and description:
    #         raise ValidationError('You already got this')

    class Meta:
        fields = ('id', 'joke_id', 'tag_id')
        ordered = True


# Note this table needs to be unique