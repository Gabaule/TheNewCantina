from . import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class Cafeteria(db.Model):
    __tablename__ = 'cafeteria'

    cafeteria_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255)) 
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    menus = db.relationship('DailyMenu', back_populates='cafeteria', lazy=True)
    reservations = db.relationship('Reservation', back_populates='cafeteria', lazy=True)

    @classmethod
    def create_cafeteria(
        cls,
        name: str
    ):
        """
        Create and add a new cafeteria to the session.
        The caller is responsible for committing the session.
        Returns the cafeteria instance.
        """
        cafeteria = cls(
            name=name
        )
        db.session.add(cafeteria)
        return cafeteria

    @classmethod
    def get_by_id(cls, cafeteria_id: int):
        """
        Retrieve a cafeteria by its ID.
        Returns the Cafeteria instance or None if not found.
        """
        return cls.query.get(cafeteria_id)

    @classmethod
    def get_all_dicts(cls):
        """
        Return all cafeterias as a list of dictionaries.
        """
        return [cafeteria.to_dict() for cafeteria in cls.query.all()]

    def update_cafeteria(
        self,
        name: str = None
    ) -> bool:
        """
        Update the cafeteria fields. Only provided fields will be updated.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if name is not None:
            self.name = name
            updated = True
        
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_cafeteria(self) -> bool:
        """
        Delete this cafeteria from the database.
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
        Return this cafeteria as a dictionary.
        """
        return {
            'cafeteria_id': self.cafeteria_id,
            'name': self.name,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }