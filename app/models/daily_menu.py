from . import db
from datetime import datetime
class DailyMenu(db.Model):
    __tablename__ = 'daily_menu'
    menu_id = db.Column(db.Integer, primary_key=True)
    cafeteria_id = db.Column(db.Integer, db.ForeignKey('cafeteria.cafeteria_id'), nullable=False)
    menu_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('DailyMenuItem', backref='menu', lazy=True)