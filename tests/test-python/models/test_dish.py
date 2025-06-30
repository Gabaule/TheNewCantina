# tests/test-python/models/test_dish.py

import pytest
from datetime import date
from app.models import db, Dish, DailyMenuItem, DailyMenu, Cafeteria, OrderItem, Reservation, AppUser
from sqlalchemy.exc import IntegrityError

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

def test_get_all_dishes_as_dicts(app):
    """Teste la méthode get_all_dicts."""
    with app.app_context():
        db.session.query(Dish).delete()
        Dish.create_dish("Plat A", "", 1, "main_course")
        Dish.create_dish("Plat B", "", 2, "main_course")
        db.session.commit()
        dishes = Dish.get_all_dicts()
        assert len(dishes) == 2
        assert dishes[0]['name'] == "Plat A"

def test_dish_delete_fails_if_in_use_by_menu_item(app):
    """Vérifie qu'un plat ne peut être supprimé s'il est dans un menu."""
    with app.app_context():
        dish = Dish.create_dish("Frites", "", 2.50, "side_dish")
        caf = Cafeteria.create_cafeteria("Caf")
        db.session.commit()
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        db.session.commit()
        DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "side_dish")
        db.session.commit()

        # Tenter de supprimer le plat maintenant qu'il est référencé
        ok = dish.delete_dish()
        assert ok is False
        assert Dish.get_by_id(dish.dish_id) is not None # Le plat doit toujours exister

def test_dish_delete_fails_if_in_use_by_order_item(app):
    """Vérifie qu'un plat ne peut être supprimé s'il est dans une commande."""
    with app.app_context():
        dish = Dish.create_dish("Pizza", "", 8.50, "main_course")
        caf = Cafeteria.create_cafeteria("Caf")
        user = AppUser.create_user("test", "del", "del@test.com", "p")
        db.session.commit()
        res = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=8.5)
        db.session.commit()
        OrderItem.create_order_item(res.reservation_id, dish.dish_id, 1, False, 8.5)
        db.session.commit()

        # Tenter de supprimer le plat
        ok = dish.delete_dish()
        assert ok is False
        assert Dish.get_by_id(dish.dish_id) is not None # Le plat doit toujours exister