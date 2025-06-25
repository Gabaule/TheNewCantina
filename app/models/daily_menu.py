from . import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class DailyMenu(db.Model):
    __tablename__ = 'daily_menu'

    menu_id = db.Column(db.Integer, primary_key=True)
    cafeteria_id = db.Column(db.Integer, db.ForeignKey('cafeteria.cafeteria_id'), nullable=False)
    menu_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (if you want to list all items of a menu)
    items = db.relationship('DailyMenuItem', backref='menu', lazy=True)

    @classmethod
    def create_menu(
        cls,
        cafeteria_id: int,
        menu_date: datetime.date
    ):
        """
        Create and insert a new daily menu into the database.
        Returns the DailyMenu instance if successful, or None if there is an error.
        """
        menu = cls(
            cafeteria_id=cafeteria_id,
            menu_date=menu_date
        )
        try:
            db.session.add(menu)
            db.session.commit()
            return menu
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_id(cls, menu_id: int):
        """
        Retrieve a daily menu by its ID.
        Returns the DailyMenu instance or None if not found.
        """
        return cls.query.get(menu_id)

    @classmethod
    def get_all_dicts(cls):
        """
        Return all daily menus as a list of dictionaries.
        """
        return [menu.to_dict() for menu in cls.query.all()]

    def update_menu(
        self,
        cafeteria_id: int = None,
        menu_date: datetime.date = None
    ) -> bool:
        """
        Update the daily menu fields. Only provided fields will be updated.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if cafeteria_id is not None:
            self.cafeteria_id = cafeteria_id
            updated = True
        if menu_date is not None:
            self.menu_date = menu_date
            updated = True
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_menu(self) -> bool:
        """
        Delete this daily menu from the database.
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
        Return this daily menu as a dictionary.
        """
        return {
            'menu_id': self.menu_id,
            'cafeteria_id': self.cafeteria_id,
            'menu_date': self.menu_date.isoformat() if self.menu_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
