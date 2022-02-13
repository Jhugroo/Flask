from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app= Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://udacitystudios@localhost:5432/example'

class Moviee(db.Model):
  __table__name = 'movies'

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(), nullable=False)
  genre = db.Column(db.String(),nullable = False)
  rating = db.Column(db.Integer)

  def __init__(self,name,genre,rating):
    self.name = name
    self.genre = genre
    self.rating = rating

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'genre': self.genre,
      'rating': self.rating,
    }

 
db.create_all()