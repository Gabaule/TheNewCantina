from . import db
from datetime import datetime
class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    cafeteria_id = db.Column(db.Integer, db.ForeignKey('cafeteria.cafeteria_id'))
    reservation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(20), default='pending')

    items = db.relationship('OrderItem', backref='reservation', lazy=True)