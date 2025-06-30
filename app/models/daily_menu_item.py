from . import db
from sqlalchemy.exc import IntegrityError

class DailyMenuItem(db.Model):
    __tablename__ = 'daily_menu_item'

    menu_item_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('daily_menu.menu_id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    dish_role = db.Column(db.String(20), nullable=False)  # e.g. 'main_course', 'side_dish', 'soup', 'drink', 'dessert'
    display_order = db.Column(db.Integer, default=1)

    # Relationships (if you want to access the menu or dish from this item)
    menu = db.relationship('DailyMenu', back_populates='items')
    dish = db.relationship('Dish', back_populates='menu_items')

    @classmethod
    def create_menu_item(
        cls,
        menu_id: int,
        dish_id: int,
        dish_role: str,
        display_order: int = 1
    ):
        """
        Create and add a new daily menu item to the session.
        The caller is responsible for committing the session.
        Returns the DailyMenuItem instance.
        """
        item = cls(
            menu_id=menu_id,
            dish_id=dish_id,
            dish_role=dish_role,
            display_order=display_order
        )
        db.session.add(item)
        return item

    @classmethod
    def get_by_id(cls, menu_item_id: int):
        """
        Retrieve a daily menu item by its ID.
        Returns the DailyMenuItem instance or None if not found.
        """
        return db.session.get(cls, menu_item_id)


    @classmethod
    def get_all_dicts(cls):
        """
        Return all daily menu items as a list of dictionaries.
        """
        return [item.to_dict() for item in cls.query.all()]

    def update_menu_item(
        self,
        menu_id: int = None,
        dish_id: int = None,
        dish_role: str = None,
        display_order: int = None
    ) -> bool:
        """
        Update the daily menu item fields. Only provided fields will be updated.
        Returns True if update is successful, False otherwise.
        """
        updated = False
        if menu_id is not None:
            self.menu_id = menu_id
            updated = True
        if dish_id is not None:
            self.dish_id = dish_id
            updated = True
        if dish_role is not None:
            self.dish_role = dish_role
            updated = True
        if display_order is not None:
            self.display_order = display_order
            updated = True
        if not updated:
            return False
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def delete_menu_item(self) -> bool:
        """
        Delete this daily menu item from the database.
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
        Return this daily menu item as a dictionary.
        """
        return {
            'menu_item_id': self.menu_item_id,
            'menu_id': self.menu_id,
            'dish_id': self.dish_id,
            'dish_role': self.dish_role,
            'display_order': self.display_order
        }