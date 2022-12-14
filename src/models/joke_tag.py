from init import db, ma
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
    # Ensure all instances are unique (the tag does not already exist for the joke)
    validation = fields.Method("is_unique_instance")
    def is_unique_instance(self, obj):
        # Count all joke_tag instances where joke_id = joke_id of the object, and tag_id = tag_id of the object passed in
        # Should be 1 if it already exists, 0 if not
        stmt = db.select(db.func.count()).select_from(Joke_tag).filter_by(joke_id=obj.joke_id, tag_id=obj.tag_id)
        exist = db.session.scalar(stmt)
        if exist:
            raise ValidationError('This joke already contains this tag')
        return True

    class Meta:
        fields = ('id', 'joke_id', 'tag_id', 'tag', 'validation')
        ordered = True

