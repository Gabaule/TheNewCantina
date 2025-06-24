from . import db
from datetime import datetime
class DailyMenuItem(db.Model):
    __tablename__ = 'daily_menu_item'
    menu_item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.menu_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    dish_role = db.Column(db.String(20), nullable=False)  # ('main_course', 'side_dish', 'soup', 'drink')
    display_order = db.Column(db.Integer, default=1)