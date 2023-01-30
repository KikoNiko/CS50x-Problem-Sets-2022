from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#Create table in our db to store our users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    recipes = db.relationship('Recipes', backref='user_recipes', passive_deletes=True)
    foods = db.relationship('FoodItems', backref='user_foods', passive_deletes=True)


# Create table for the food inventory
class FoodItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    category = db.Column(db.String(50))
    units = db.Column(db.String(20))
    quantity = db.Column(db.String(20))
    owner = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, fname, category, units, quantity, owner):
        self.fname = fname
        self.category = category
        self.units = units
        self.quantity = quantity
        self.owner = owner


# Create table to save recipes
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(150))
    title = db.Column(db.String(150))
    url = db.Column(db.Text, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, title, uri, url, owner):
        self.uri = uri
        self.title = title
        self.url = url
        self.owner = owner
        
        