from flask_sqlalchemy import SQLAlchemy
from app import db

class Weather(db.Model):
    """creating a model for the weather table"""

    __tablename__ = 'weather'
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String,nullable=False)
    country = db.Column(db.String,nullable=False)
    temperature = db.Column(db.Float,nullable=False)
    description = db.Column(db.String,nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'City: {self.city}, Country: {self.country}, Date: {self.date}, Temperature: {self.temperature}, Description: {self.description}'