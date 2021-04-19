from . import *

class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  shoe_id = db.Column(db.Integer, db.ForeignKey('shoe.id'), nullable=False)
  text = db.Column(db.String(512), nullable =False)

  def __init__(self, **kwargs):
    self.text = kwargs.get('text', None)

  def __repr__(self):
    return str(self.__dict__)


class ReviewSchema(ModelSchema):
  class Meta:
    model = Review
