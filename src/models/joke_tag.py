from init import db, ma
from marshmallow import validates
from marshmallow.exceptions import ValidationError
from marshmallow import fields
from sqlalchemy import CheckConstraint


class Joke_tag(db.Model):
    __tablename__ = 'joke_tags'
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('jokes.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

    joke = db.relationship('Joke', back_populates='joke_tags')
    tag = db.relationship('Tag', back_populates='joke_tags')

class Joke_tagSchema(ma.Schema):
    tag = fields.Nested('TagSchema', only=['name'])
    # Ensure all instances are unique
    validation = fields.Method("is_unique_instance")
    
    def is_unique_instance(self, obj):
        stmt = db.select(db.func.count()).select_from(Joke_tag).filter_by(joke_id=obj.joke_id, tag_id=obj.tag_id)
        exist = db.session.scalar(stmt)
        if exist >= 1:
            raise ValidationError('This particular instance already exists')
        return True

    class Meta:
        fields = ('id', 'joke_id', 'tag_id', 'tag', 'validation')
        ordered = True


# Note this table needs to be unique