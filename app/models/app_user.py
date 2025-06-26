from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class AppUser(db.Model):
    __tablename__ = 'app_user'

    user_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password only!
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = db.relationship('Reservation', back_populates='user', lazy=True)

    @classmethod
    def create_user(
        cls,
        last_name: str,
        first_name: str,
        email: str,
        password: str,
        role: str = 'student',
        balance: float = 0.00
    ):
        """
        Create and add a new user to the session with a hashed password.
        The caller is responsible for committing the session.
        Returns the user instance.
        """
        password_hash = generate_password_hash(password)
        user = cls(
            last_name=last_name,
            first_name=first_name,
            email=email,
            password=password_hash,
            role=role,
            balance=balance
        )
        db.session.add(user)
        return user

    @classmethod
    def get_by_id(cls, user_id: int):
        """
        Retrieve a user by their user_id.
        Returns the AppUser instance or None if not found.
        """
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email: str):
        """
        Retrieve a user by their email.
        Returns the AppUser instance or None if not found.
        """
        return cls.query.filter_by(email=email).first()

    def update_user(
        self,
        last_name: str = None,
        first_name: str = None,
        email: str = None,
        password: str = None,
        role: str = None,
        balance: float = None
    ) -> bool:
        """
        Update the user's fields. Only provided fields will be updated.
        If password is provided, it will be hashed.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if last_name is not None:
            self.last_name = last_name
            updated = True
        if first_name is not None:
            self.first_name = first_name
            updated = True
        if email is not None:
            self.email = email
            updated = True
        if password is not None:
            self.password = generate_password_hash(password)
            updated = True
        if role is not None:
            self.role = role
            updated = True
        if balance is not None:
            self.balance = balance
            updated = True
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_user(self) -> bool:
        """
        Delete this user from the database (hard delete).
        All related reservations will be deleted via ON DELETE CASCADE.
        Returns True if successful, False otherwise.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def verify_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password hash.
        Returns True if it matches, False otherwise.
        """
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Return this user as a dictionary (excluding sensitive fields like password)."""
        return {
            'user_id': self.user_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'email': self.email,
            'balance': float(self.balance),
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
    @classmethod
    def get_all_dicts(cls):
        """Return all users as a list of dictionaries (excluding password)."""
        return [user.to_dict() for user in cls.query.all()]