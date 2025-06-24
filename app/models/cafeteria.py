from . import db
from datetime import datetime

class Cafeteria(db.Model):
    __tablename__ = 'cafeteria'
    cafeteria_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    menus = db.relationship('DailyMenu', backref='cafeteria', lazy=True)
    reservations = db.relationship('Reservation', backref='cafeteria', lazy=True)