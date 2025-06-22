# models/dish.py
from models.base_model import BaseModel, db

class Dish(BaseModel):
    __tablename__ = 'dishes'
    
    dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dine_in_price = db.Column(db.Numeric(10, 2), nullable=False)
    takeaway_price = db.Column(db.Numeric(10, 2), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    
    # Relationships
    order_details = db.relationship('OrderDetail', backref='dish', lazy=True)
    
    def __repr__(self):
        return f'<Dish {self.dish_id}: {self.name}>'
    
    # Enhanced CREATE operations
    @classmethod
    def create_dish(cls, name, dine_in_price, takeaway_price, description=None, is_available=True):
        """Create a new dish"""
        return cls.create(
            name=name,
            description=description,
            dine_in_price=dine_in_price,
            takeaway_price=takeaway_price,
            is_available=is_available
        )
    
    # Enhanced READ operations
    @classmethod
    def get_available(cls):
        """Get all available dishes"""
        return cls.get_by(is_available=True)
    
    @classmethod
    def get_unavailable(cls):
        """Get all unavailable dishes"""
        return cls.get_by(is_available=False)
    
    @classmethod
    def search_by_name(cls, name):
        """Search dishes by name"""
        return cls.query.filter(cls.name.contains(name)).all()
    
    @classmethod
    def get_by_price_range(cls, min_price=0, max_price=None, is_takeaway=False):
        """Get dishes within price range"""
        price_column = cls.takeaway_price if is_takeaway else cls.dine_in_price
        query = cls.query.filter(price_column >= min_price)
        if max_price:
            query = query.filter(price_column <= max_price)
        return query.all()
    
    @classmethod
    def get_popular_dishes(cls, limit=10):
        """Get most ordered dishes"""
        from models.order_detail import OrderDetail
        from sqlalchemy import func
        return cls.query.join(OrderDetail).group_by(cls.dish_id).order_by(
            func.sum(OrderDetail.quantity).desc()
        ).limit(limit).all()
    
    # Enhanced UPDATE operations
    def update_availability(self, is_available):
        """Update dish availability"""
        return self.update(is_available=is_available)
    
    def update_prices(self, dine_in_price=None, takeaway_price=None):
        """Update dish prices"""
        data = {}
        if dine_in_price is not None:
            data['dine_in_price'] = dine_in_price
        if takeaway_price is not None:
            data['takeaway_price'] = takeaway_price
        return self.update(**data)
    
    def update_info(self, name=None, description=None):
        """Update dish information"""
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        return self.update(**data)
    
    # Business logic methods
    def get_price(self, is_takeaway=False):
        """Get appropriate price based on service type"""
        return self.takeaway_price if is_takeaway else self.dine_in_price
    
    def toggle_availability(self):
        """Toggle dish availability"""
        return self.update_availability(not self.is_available)
    
    def get_order_count(self):
        """Get total number of times this dish was ordered"""
        from models.order_detail import OrderDetail
        from sqlalchemy import func
        result = db.session.query(func.sum(OrderDetail.quantity)).filter(
            OrderDetail.dish_id == self.dish_id
        ).scalar()
        return result or 0
