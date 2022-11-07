from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    joke_tags = db.relationship('Joke_tag', back_populates='tag', cascade='all, delete')


class TagSchema(ma.Schema):
    # Repeated maximum length for better Error display message handling
    # Limit 45 as longest english word is 45 letters 
    name = fields.String(required=True, validate=Length(max=45, error='tags can only be up to 45 characters long'))

    class Meta:
        fields = ('id', 'name', 'description')
        ordered = True

