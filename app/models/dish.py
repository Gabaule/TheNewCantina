from . import db
from datetime import datetime
class Dish(db.Model):
    __tablename__ = 'dish'
    dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dine_in_price = db.Column(db.Numeric(10,2), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    dish_type = db.Column(db.String(20), nullable=False)  # ('main_course', 'side_dish', 'soup', 'drink')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    menu_items = db.relationship('DailyMenuItem', backref='dish', lazy=True)
    order_items = db.relationship('OrderItem', backref='dish', lazy=True)