from . import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservation'

    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    cafeteria_id = db.Column(db.Integer, db.ForeignKey('cafeteria.cafeteria_id'))
    reservation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(20), default='pending')

    # Relationships for navigation
    user = db.relationship('AppUser', backref=db.backref('reservations', lazy=True))
    cafeteria = db.relationship('Cafeteria', backref=db.backref('reservations', lazy=True))
    order_items = db.relationship('OrderItem', backref='reservation', lazy=True)

    @classmethod
    def create_reservation(
        cls,
        user_id: int,
        cafeteria_id: int,
        reservation_datetime: datetime = None,
        total: float = 0.00,
        status: str = 'pending'
    ):
        """
        Create and insert a new reservation into the database.
        Returns the Reservation instance if successful, or None if there is an error.
        """
        reservation = cls(
            user_id=user_id,
            cafeteria_id=cafeteria_id,
            reservation_datetime=reservation_datetime or datetime.utcnow(),
            total=total,
            status=status
        )
        try:
            db.session.add(reservation)
            db.session.commit()
            return reservation
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_id(cls, reservation_id: int):
        """
        Retrieve a reservation by its ID.
        Returns the Reservation instance or None if not found.
        """
        return cls.query.get(reservation_id)

    @classmethod
    def get_all_dicts(cls):
        """
        Return all reservations as a list of dictionaries.
        """
        return [res.to_dict() for res in cls.query.all()]

    def update_reservation(
        self,
        user_id: int = None,
        cafeteria_id: int = None,
        reservation_datetime: datetime = None,
        total: float = None,
        status: str = None
    ) -> bool:
        """
        Update the reservation fields. Only provided fields will be updated.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if user_id is not None:
            self.user_id = user_id
            updated = True
        if cafeteria_id is not None:
            self.cafeteria_id = cafeteria_id
            updated = True
        if reservation_datetime is not None:
            self.reservation_datetime = reservation_datetime
            updated = True
        if total is not None:
            self.total = total
            updated = True
        if status is not None:
            self.status = status
            updated = True
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_reservation(self) -> bool:
        """
        Delete this reservation from the database.
        Returns True if successful, False otherwise.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def to_dict(self):
        """
        Return this reservation as a dictionary.
        """
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'cafeteria_id': self.cafeteria_id,
            'reservation_datetime': self.reservation_datetime.isoformat() if self.reservation_datetime else None,
            'total': float(self.total),
            'status': self.status
        }
    
    @classmethod
    def get_by_user(cls, user_id: int):
        """
        Retrieve all reservations for a given user_id.
        Returns a list of Reservation instances.
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_user_dicts(cls, user_id: int):
        """
        Retrieve all reservations for a given user_id as a list of dicts.
        """
        return [res.to_dict() for res in cls.query.filter_by(user_id=user_id).all()]

