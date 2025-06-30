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

def test_update_menu_with_no_data(app):
    """Teste que l'appel à update_menu sans données renvoie False."""
    with app.app_context():
        caf = Cafeteria.create_cafeteria("C4")
        db.session.commit()
        menu = DailyMenu.create_menu(caf.cafeteria_id, date.today())
        db.session.commit()
        assert menu.update_menu() is False

def test_menu_uniqueness_constraint_on_update(app):
    """Vérifie la contrainte d'unicité (cafeteria_id, menu_date) lors d'une mise à jour."""
    with app.app_context():
        caf1 = Cafeteria.create_cafeteria("Caf 1")
        caf2 = Cafeteria.create_cafeteria("Caf 2")
        db.session.commit()

        # Menu existant pour caf1 à une date donnée
        DailyMenu.create_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
        
        # Autre menu pour caf2 qu'on va essayer de déplacer
        menu_to_update = DailyMenu.create_menu(cafeteria_id=caf2.cafeteria_id, menu_date=date(2030, 1, 2))
        db.session.commit()

        # Tenter de déplacer le menu vers une date/cafeteria déjà prise
        ok = menu_to_update.update_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
        assert ok is False # La méthode doit retourner False en cas d'échec d'intégrité

def test_get_all_menus_as_dicts(app):
    """Teste la méthode utilitaire get_all_dicts pour DailyMenu."""
    with app.app_context():
        db.session.query(DailyMenu).delete()
        caf = Cafeteria.create_cafeteria("C5")
        db.session.commit()
        DailyMenu.create_menu(caf.cafeteria_id, date(2030,1,1))
        DailyMenu.create_menu(caf.cafeteria_id, date(2030,1,2))
        db.session.commit()
        menus = DailyMenu.get_all_dicts()
        assert len(menus) == 2