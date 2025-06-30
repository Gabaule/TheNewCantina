from . import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class Dish(db.Model):
    __tablename__ = 'dish'
    dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dine_in_price = db.Column(db.Numeric(10,2), nullable=False)
    dish_type = db.Column(db.String(20), nullable=False)  # ('main_course', 'side_dish', 'soup', 'drink', 'dessert')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    menu_items = db.relationship('DailyMenuItem', back_populates='dish', lazy=True)
    order_items = db.relationship('OrderItem', back_populates='dish', lazy=True)

    def to_dict(self):
        return {
            'dish_id': self.dish_id,
            'name': self.name,
            'description': self.description,
            'dine_in_price': float(self.dine_in_price),
            'dish_type': self.dish_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
    }

    @classmethod
    def get_all_dicts(cls):
        """Return all dishes as a list of dictionaries, ordered by name."""
        return [dish.to_dict() for dish in cls.query.order_by(cls.name).all()]

    def update_from_dict(self, data):
        for field in ['name', 'description', 'dine_in_price', 'dish_type']:
            if field in data:
                setattr(self, field, data[field])
    
    @classmethod
    def get_by_id(cls, dish_id):
        return db.session.get(cls, dish_id)
    
    @classmethod
    def create_dish(cls, name, description, dine_in_price, dish_type):
        """
        Create and add a new dish to the session.
        The caller is responsible for committing the session.
        Returns the dish instance.
        """
        dish = cls(
            name=name,
            description=description,
            dine_in_price=dine_in_price,
            dish_type=dish_type
        )
        db.session.add(dish)
        return dish

    # This method is used by the seeder. It doesn't add to the session
    # to allow for bulk adding with db.session.add_all().
    @classmethod
    def create_from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data.get('description'),
            dine_in_price=data['dine_in_price'],
            dish_type=data['dish_type']
        )
    
    def delete_dish(self) -> bool:
        """
        Delete this dish from the database.
        Returns True if successful, False otherwise.
        Catches IntegrityError if the dish is referenced by a foreign key.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False
        except Exception:
            db.session.rollback()
            return False