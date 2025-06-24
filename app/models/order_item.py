from . import db
from datetime import datetime
class OrderItem(db.Model):
    __tablename__ = 'order_item'
    item_id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_takeaway = db.Column(db.Boolean, nullable=False)
    applied_price = db.Column(db.Numeric(10,2), nullable=False)