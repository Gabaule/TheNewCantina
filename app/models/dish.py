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

    def to_dict(self):
        return {
            'dish_id': self.dish_id,
            'name': self.name,
            'description': self.description,
            'dine_in_price': float(self.dine_in_price),
            'is_available': self.is_available,
            'dish_type': self.dish_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
    }

    def toggle_availability(self):
        self.is_available = not self.is_available
    
    def update_from_dict(self, data):
        for field in ['name', 'description', 'dine_in_price', 'is_available', 'dish_type']:
            if field in data:
                setattr(self, field, data[field])
    
    @classmethod
    def get_by_id(cls, dish_id):
        return cls.query.get(dish_id)
    
    @classmethod
    def get_available(cls):
        return cls.query.filter_by(is_available=True).all()
    
    @classmethod
    def create_from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data.get('description'),
            dine_in_price=data['dine_in_price'],
            is_available=data.get('is_available', True),
            dish_type=data['dish_type']
        )
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()




