# models/user.py
from .base_model import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import func
from decimal import Decimal

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    # Define columns (inherited created_at, updated_at from BaseModel)
    user_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        # Hash password if provided
        if 'password' in kwargs:
            kwargs['password'] = generate_password_hash(kwargs['password'])
        super().__init__(**kwargs)
    
    # Override get_id for Flask-Login
    def get_id(self):
        return str(self.user_id)
    
    # Password methods
    def set_password(self, password):
        """Set password hash"""
        self.password = generate_password_hash(password)
        return self
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password, password)
    
    # Balance operations
    def add_balance(self, amount):
        """Add money to user balance"""
        if amount > 0:
            self.balance = (self.balance or 0) + Decimal(str(amount))
            return self.save()
        raise ValueError("Amount must be positive")
    
    def deduct_balance(self, amount):
        """Deduct money from user balance"""
        if amount > 0:
            current_balance = self.balance or 0
            if current_balance >= Decimal(str(amount)):
                self.balance = current_balance - Decimal(str(amount))
                return self.save()
            else:
                raise ValueError("Insufficient balance")
        raise ValueError("Amount must be positive")
    
    def has_sufficient_balance(self, amount):
        """Check if user has sufficient balance"""
        return (self.balance or 0) >= Decimal(str(amount))
    
    # User-specific query methods
    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def email_exists(cls, email):
        """Check if email already exists"""
        return cls.query.filter_by(email=email).first() is not None
    
    @classmethod
    def search_users(cls, search_term, limit=None):
        """Search users by name or email"""
        search_pattern = f"%{search_term}%"
        query = cls.query.filter(
            db.or_(
                cls.first_name.ilike(search_pattern),
                cls.last_name.ilike(search_pattern),
                cls.email.ilike(search_pattern)
            )
        )
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_users_with_low_balance(cls, threshold=5.00):
        """Get users with balance below threshold"""
        return cls.query.filter(cls.balance < threshold).all()
    
    @classmethod
    def get_total_balance(cls):
        """Get sum of all user balances"""
        result = db.session.query(func.sum(cls.balance)).scalar()
        return result or 0
    
    # Override to_dict to exclude password
    def to_dict(self, include_password=False):
        """Convert model to dictionary"""
        data = super().to_dict()
        if not include_password:
            data.pop('password', None)
        return data
    
    def to_public_dict(self):
        """Convert to dict with only public information"""
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'balance': float(self.balance) if self.balance else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def balance_float(self):
        """Get balance as float"""
        return float(self.balance) if self.balance else 0.0
    
    def __repr__(self):
        return f'<User {self.email}>'