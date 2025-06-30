# tests/test-python/models/test_dish.py

from app.models.dish import Dish
from app.models import db

def test_create_dish(app):
    with app.app_context():
        dish = Dish.create_dish("DishName", "Desc", 5.0, "main_course")
        db.session.commit()
        assert dish.dish_id is not None

def test_update_from_dict(app):
    with app.app_context():
        dish = Dish.create_dish("Old", "OldDesc", 1.0, "main_course")
        db.session.commit()
        dish.update_from_dict({"name": "New", "dine_in_price": 3.2})
        assert dish.name == "New"
        assert float(dish.dine_in_price) == 3.2

def test_get_by_id(app):
    with app.app_context():
        dish = Dish.create_dish("D", "D", 1.0, "main_course")
        db.session.commit()
        assert Dish.get_by_id(dish.dish_id) == dish

def test_delete_dish(app):
    with app.app_context():
        dish = Dish.create_dish("Del", "Del", 1.0, "main_course")
        db.session.commit()
        id_ = dish.dish_id
        assert dish.delete_dish()
        assert Dish.get_by_id(id_) is None
