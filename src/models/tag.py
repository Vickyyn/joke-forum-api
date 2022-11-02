from init import db, ma

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.Text)


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')
        ordered = True

# Limit 50 as longest english word is 45 letters 