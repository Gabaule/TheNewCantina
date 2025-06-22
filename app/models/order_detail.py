# models/order_detail.py
from models.base_model import BaseModel, db
from sqlalchemy import func

class OrderDetail(BaseModel):
    __tablename__ = 'order_details'
    
    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.dish_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_takeaway = db.Column(db.Boolean, nullable=False)
    applied_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderDetail {self.detail_id}: {self.quantity}x Dish {self.dish_id}>'
    
    # Enhanced CREATE operations
    @classmethod
    def create_detail(cls, order_id, dish_id, quantity, is_takeaway, applied_price):
        """Create a new order detail"""
        return cls.create(
            order_id=order_id,
            dish_id=dish_id,
            quantity=quantity,
            is_takeaway=is_takeaway,
            applied_price=applied_price
        )
    
    @classmethod
    def create_from_dish(cls, order_id, dish, quantity, is_takeaway):
        """Create order detail from dish"""
        return cls.create_detail(
            order_id=order_id,
            dish_id=dish.dish_id,
            quantity=quantity,
            is_takeaway=is_takeaway,
            applied_price=dish.get_price(is_takeaway)
        )
    
    # Enhanced READ operations
    @classmethod
    def get_order_details(cls, order_id):
        """Get all details for an order"""
        return cls.get_by(order_id=order_id)
    
    @classmethod
    def get_dish_order_details(cls, dish_id):
        """Get all order details for a specific dish"""
        return cls.get_by(dish_id=dish_id)
    
    @classmethod
    def get_takeaway_details(cls, order_id=None):
        """Get takeaway order details"""
        query = cls.query.filter_by(is_takeaway=True)
        if order_id:
            query = query.filter_by(order_id=order_id)
        return query.all()
    
    @classmethod
    def get_dine_in_details(cls, order_id=None):
        """Get dine-in order details"""
        query = cls.query.filter_by(is_takeaway=False)
        if order_id:
            query = query.filter_by(order_id=order_id)
        return query.all()
    
    @classmethod
    def get_popular_dishes_stats(cls, limit=10):
        """Get statistics for most popular dishes"""
        return cls.query.join(cls.dish).group_by(cls.dish_id).order_by(
            func.sum(cls.quantity).desc()
        ).limit(limit).all()
    
    # Enhanced UPDATE operations
    def update_quantity(self, quantity):
        """Update quantity and recalculate if needed"""
        self.update(quantity=quantity)
        # Recalculate order total
        self.order.calculate_total()
        return self
    
    def update_service_type(self, is_takeaway):
        """Update service type and adjust price"""
        new_price = self.dish.get_price(is_takeaway)
        return self.update(is_takeaway=is_takeaway, applied_price=new_price)
    
    # Business logic methods
    def get_subtotal(self):
        """Calculate subtotal for this order detail"""
        return self.applied_price * self.quantity
    
    def get_service_type_display(self):
        """Get human-readable service type"""
        return "Takeaway" if self.is_takeaway else "Dine-in"