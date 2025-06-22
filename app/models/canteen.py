# models/canteen.py
from models.base_model import BaseModel, db

class Canteen(BaseModel):
    __tablename__ = 'canteens'
    
    canteen_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    
    # Relationships
    orders = db.relationship('Order', backref='canteen', lazy=True)
    
    def __repr__(self):
        return f'<Canteen {self.canteen_id}: {self.name}>'
    
    # Enhanced CREATE operations
    @classmethod
    def create_canteen(cls, name, address=None, phone=None):
        """Create a new canteen"""
        return cls.create(name=name, address=address, phone=phone)
    
    # Enhanced READ operations
    @classmethod
    def get_all_active(cls):
        """Get all active canteens"""
        return cls.get_all()
    
    @classmethod
    def search_by_name(cls, name):
        """Search canteens by name"""
        return cls.query.filter(cls.name.contains(name)).all()
    
    @classmethod
    def get_canteens_with_orders(cls):
        """Get canteens that have orders"""
        return cls.query.join(cls.orders).distinct().all()
    
    # Enhanced UPDATE operations
    def update_info(self, name=None, address=None, phone=None):
        """Update canteen information"""
        data = {}
        if name:
            data['name'] = name
        if address:
            data['address'] = address
        if phone:
            data['phone'] = phone
        return self.update(**data)
    
    # Business logic methods
    def get_orders_count(self):
        """Get total number of orders for this canteen"""
        return len(self.orders)
    
    def get_recent_orders(self, days=7):
        """Get recent orders for this canteen"""
        from datetime import datetime, timedelta
        from models.order import Order
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return Order.query.filter(
            Order.canteen_id == self.canteen_id,
            Order.order_date >= cutoff_date
        ).all()
