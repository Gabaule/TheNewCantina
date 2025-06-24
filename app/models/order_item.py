from . import db
from datetime import datetime
class OrderItem(db.Model):
    __tablename__ = 'order_item'
    item_id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_takeaway = db.Column(db.Boolean, nullable=False)
    applied_price = db.Column(db.Numeric(10,2), nullable=False)

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'reservation_id': self.reservation_id,
            'dish_id': self.dish_id,
            'quantity': self.quantity,
            'is_takeaway': self.is_takeaway,
            'applied_price': float(self.applied_price),
        }

    # -------------------
    # Create from dict
    # -------------------
    @classmethod
    def create_from_dict(cls, data):
        return cls(
            reservation_id=data['reservation_id'],
            dish_id=data['dish_id'],
            quantity=data.get('quantity', 1),
            is_takeaway=data['is_takeaway'],
            applied_price=data['applied_price']
        )

    # -------------------
    # Read by ID
    # -------------------
    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.get(item_id)

    # -------------------
    # Read all items for a reservation
    # -------------------
    @classmethod
    def get_by_reservation(cls, reservation_id):
        return cls.query.filter_by(reservation_id=reservation_id).all()

    # -------------------
    # Update from dict
    # -------------------
    def update_from_dict(self, data):
        for field in ['reservation_id', 'dish_id', 'quantity', 'is_takeaway', 'applied_price']:
            if field in data:
                setattr(self, field, data[field])

    # -------------------
    # Delete method
    # -------------------
    def delete(self):
        db.session.delete(self)
        db.session.commit()