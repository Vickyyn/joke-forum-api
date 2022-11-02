from init import db, ma

class Joke(db.Model):
    __tablename__ = 'jokes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))


class JokeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date', 'owner')
        ordered = True
