# tests/test-python/models/test_daily_menu.py

from app.models.daily_menu import DailyMenu
from app.models.cafeteria import Cafeteria
from app.models import db
from datetime import date

def test_create_menu(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("C")
        db.session.commit()
        menu = DailyMenu.create_menu(cafeteria_id=caf.cafeteria_id, menu_date=date.today())
        db.session.commit()
        assert menu.menu_id is not None

def test_update_menu(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("C2")
        db.session.commit()
        menu = DailyMenu.create_menu(cafeteria_id=caf.cafeteria_id, menu_date=date.today())
        db.session.commit()
        ok = menu.update_menu(menu_date=date(2030,1,1))
        assert ok
        assert menu.menu_date == date(2030,1,1)

def test_delete_menu(app):
    with app.app_context():
        caf = Cafeteria.create_cafeteria("C3")
        db.session.commit()
        menu = DailyMenu.create_menu(cafeteria_id=caf.cafeteria_id, menu_date=date.today())
        db.session.commit()
        id_ = menu.menu_id
        assert menu.delete_menu()
        assert DailyMenu.get_by_id(id_) is None
