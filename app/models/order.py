# models/order.py
from models.base_model import BaseModel, db
from datetime import datetime, timedelta
from sqlalchemy import func

class Order(BaseModel):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    canteen_id = db.Column(db.Integer, db.ForeignKey('canteens.canteen_id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    
    # Relationships
    order_details = db.relationship('OrderDetail', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_id}: {self.status} - €{self.total}>'
    
    # Enhanced CREATE operations
    @classmethod
    def create_order(cls, user_id, canteen_id, total=0.00, status='pending'):
        """Create a new order"""
        return cls.create(
            user_id=user_id,
            canteen_id=canteen_id,
            total=total,
            status=status
        )
    
    # Enhanced READ operations
    @classmethod
    def get_user_orders(cls, user_id, limit=None, status=None):
        """Get orders for a specific user"""
        query = cls.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(cls.order_date.desc())
        return query.limit(limit).all() if limit else query.all()
    
    @classmethod
    def get_canteen_orders(cls, canteen_id, limit=None, status=None):
        """Get orders for a specific canteen"""
        query = cls.query.filter_by(canteen_id=canteen_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(cls.order_date.desc())
        return query.limit(limit).all() if limit else query.all()
    
    @classmethod
    def get_orders_by_status(cls, status):
        """Get all orders with specific status"""
        return cls.get_by(status=status)
    
    @classmethod
    def get_pending_orders(cls):
        """Get all pending orders"""
        return cls.get_orders_by_status('pending')
    
    @classmethod
    def get_completed_orders(cls):
        """Get all completed orders"""
        return cls.get_orders_by_status('completed')
    
    @classmethod
    def get_orders_by_date_range(cls, start_date, end_date):
        """Get orders within date range"""
        return cls.query.filter(
            cls.order_date >= start_date,
            cls.order_date <= end_date
        ).all()
    
    @classmethod
    def get_todays_orders(cls):
        """Get today's orders"""
        today = datetime.utcnow().date()
        return cls.query.filter(func.date(cls.order_date) == today).all()
    
    @classmethod
    def get_orders_summary(cls, days=30):
        """Get orders summary for last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return {
            'total_orders': cls.query.filter(cls.order_date >= cutoff_date).count(),
            'total_revenue': cls.query.filter(cls.order_date >= cutoff_date).with_entities(func.sum(cls.total)).scalar() or 0,
            'pending_orders': cls.query.filter(cls.order_date >= cutoff_date, cls.status == 'pending').count(),
            'completed_orders': cls.query.filter(cls.order_date >= cutoff_date, cls.status == 'completed').count()
        }
    
    # Enhanced UPDATE operations
    def update_status(self, status):
        """Update order status"""
        return self.update(status=status)
    
    def update_total(self, total):
        """Update order total"""
        return self.update(total=total)
    
    def mark_completed(self):
        """Mark order as completed"""
        return self.update_status('completed')
    
    def mark_cancelled(self):
        """Mark order as cancelled"""
        return self.update_status('cancelled')
    
    def mark_confirmed(self):
        """Mark order as confirmed"""
        return self.update_status('confirmed')
    
    # Business logic methods
    def calculate_total(self):
        """Calculate total from order details"""
        total = sum(detail.get_subtotal() for detail in self.order_details)
        self.total = total
        self.save()
        return total
    
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def can_be_modified(self):
        """Check if order can be modified"""
        return self.status == 'pending'
    
    def get_items_count(self):
        """Get total number of items in order"""
        return sum(detail.quantity for detail in self.order_details)
