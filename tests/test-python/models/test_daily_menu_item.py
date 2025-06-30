# tests/test-python/models/test_daily_menu_item.py

from app.models.daily_menu import DailyMenu
from app.models.cafeteria import Cafeteria
from app.models.dish import Dish
from app.models.daily_menu_item import DailyMenuItem
from app.models import db
from datetime import date

def test_create_menu_item(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("DMI")
        db.session.commit()
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        dish = Dish.create_dish("X", "desc", 1, "main_course")
        db.session.commit()
        item = DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "main_course", 1)
        db.session.commit()
        assert item.menu_item_id is not None

def test_update_menu_item(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("DMI2")
        db.session.commit()
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        dish = Dish.create_dish("X", "desc", 1, "main_course")
        db.session.commit()
        item = DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "main_course", 1)
        db.session.commit()
        ok = item.update_menu_item(display_order=5)
        assert ok
        assert item.display_order == 5

def test_delete_menu_item(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("DMI3")
        db.session.commit()
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        dish = Dish.create_dish("X", "desc", 1, "main_course")
        db.session.commit()
        item = DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "main_course", 1)
        db.session.commit()
        id_ = item.menu_item_id
        assert item.delete_menu_item()
        assert DailyMenuItem.get_by_id(id_) is None

def test_update_menu_item_with_no_data(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("DMI4")
        dish = Dish.create_dish("D4", "", 1, "main_course")
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        db.session.commit()
        item = DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "main_course")
        db.session.commit()
        assert item.update_menu_item() is False

def test_get_all_menu_items_as_dicts(app):
    with app.app_context():
        db.session.query(DailyMenuItem).delete()
        caf = Cafeteria.create_cafeteria("DMI5")
        dish = Dish.create_dish("D5", "", 1, "main_course")
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        db.session.commit()
        DailyMenuItem.create_menu_item(menu.menu_id, dish.dish_id, "main_course")
        db.session.commit()
        items = DailyMenuItem.get_all_dicts()
        assert len(items) == 1