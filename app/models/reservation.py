from . import db
from datetime import datetime
class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    cafeteria_id = db.Column(db.Integer, db.ForeignKey('cafeteria.cafeteria_id'))
    reservation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(20), default='pending')

    items = db.relationship('OrderItem', backref='reservation', lazy=True)

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'cafeteria_id': self.cafeteria_id,
            'reservation_datetime': self.reservation_datetime.isoformat(),
            'total': float(self.total),
            'status': self.status,
            'items': [item.to_dict() for item in self.items]  # Assuming OrderItem has to_dict
        }

    # -------------------
    # Create from dict
    # -------------------
    @classmethod
    def create_from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            cafeteria_id=data.get('cafeteria_id'),
            reservation_datetime=data.get('reservation_datetime', datetime.utcnow()),
            total=data['total'],
            status=data.get('status', 'pending')
        )

    # -------------------
    # Read by ID
    # -------------------
    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.get(reservation_id)

    # -------------------
    # Read all by user
    # -------------------
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # -------------------
    # Update from dict
    # -------------------
    def update_from_dict(self, data):
        for field in ['user_id', 'cafeteria_id', 'reservation_datetime', 'total', 'status']:
            if field in data:
                setattr(self, field, data[field])

    # -------------------
    # Delete method
    # -------------------
    def delete(self):
        db.session.delete(self)
        db.session.commit()