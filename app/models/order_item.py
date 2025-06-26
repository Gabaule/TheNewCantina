from . import db
from sqlalchemy.exc import IntegrityError

class OrderItem(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.reservation_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_takeaway = db.Column(db.Boolean, nullable=False)
    applied_price = db.Column(db.Numeric(10,2), nullable=False)

    # Relationships (optional, for navigation)
    reservation = db.relationship('Reservation', back_populates='order_items')
    dish = db.relationship('Dish', back_populates='order_items')

    @classmethod
    def create_order_item(
        cls,
        reservation_id: int,
        dish_id: int,
        quantity: int = 1,
        is_takeaway: bool = False,
        applied_price: float = 0.00
    ):
        """
        Create and add a new order item to the session.
        The caller is responsible for committing the session.
        Returns the OrderItem instance.
        """
        item = cls(
            reservation_id=reservation_id,
            dish_id=dish_id,
            quantity=quantity,
            is_takeaway=is_takeaway,
            applied_price=applied_price
        )
        db.session.add(item)
        return item

    @classmethod
    def get_by_id(cls, item_id: int):
        """
        Retrieve an order item by its ID.
        Returns the OrderItem instance or None if not found.
        """
        return cls.query.get(item_id)

    @classmethod
    def get_all_dicts(cls):
        """
        Return all order items as a list of dictionaries.
        """
        return [item.to_dict() for item in cls.query.all()]

    def update_order_item(
        self,
        reservation_id: int = None,
        dish_id: int = None,
        quantity: int = None,
        is_takeaway: bool = None,
        applied_price: float = None
    ) -> bool:
        """
        Update the order item fields. Only provided fields will be updated.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if reservation_id is not None:
            self.reservation_id = reservation_id
            updated = True
        if dish_id is not None:
            self.dish_id = dish_id
            updated = True
        if quantity is not None:
            self.quantity = quantity
            updated = True
        if is_takeaway is not None:
            self.is_takeaway = is_takeaway
            updated = True
        if applied_price is not None:
            self.applied_price = applied_price
            updated = True
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_order_item(self) -> bool:
        """
        Delete this order item from the database.
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
        Return this order item as a dictionary.
        """
        return {
            'item_id': self.item_id,
            'reservation_id': self.reservation_id,
            'dish_id': self.dish_id,
            'quantity': self.quantity,
            'is_takeaway': self.is_takeaway,
            'applied_price': float(self.applied_price)
        }