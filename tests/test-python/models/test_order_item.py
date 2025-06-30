# tests/test-python/models/test_order_item.py

from app.models.order_item import OrderItem
from app.models.reservation import Reservation
from app.models.dish import Dish
from app.models.app_user import AppUser
from app.models.cafeteria import Cafeteria
from app.models import db

def test_create_order_item(app):
    with app.app_context():
        user = AppUser.create_user("OI", "User", "oi@ex.com", "pw")
        caf = Cafeteria.create_cafeteria("OI Caf")
        db.session.commit()
        r = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=1, status="pending")
        d = Dish.create_dish("DishOI", "desc", 5.0, "main_course")
        db.session.commit()
        oi = OrderItem.create_order_item(reservation_id=r.reservation_id, dish_id=d.dish_id, quantity=2, is_takeaway=False, applied_price=5.0)
        db.session.commit()
        assert oi.item_id is not None

def test_update_order_item(app):
    with app.app_context():
        user = AppUser.create_user("OI2", "User", "oi2@ex.com", "pw")
        caf = Cafeteria.create_cafeteria("OICaf2")
        db.session.commit()
        r = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=1, status="pending")
        d = Dish.create_dish("DishOI2", "desc", 5.0, "main_course")
        db.session.commit()
        oi = OrderItem.create_order_item(reservation_id=r.reservation_id, dish_id=d.dish_id, quantity=2, is_takeaway=False, applied_price=5.0)
        db.session.commit()
        ok = oi.update_order_item(quantity=4, is_takeaway=True)
        assert ok
        assert oi.quantity == 4
        assert oi.is_takeaway

def test_delete_order_item(app):
    with app.app_context():
        user = AppUser.create_user("OI3", "User", "oi3@ex.com", "pw")
        caf = Cafeteria.create_cafeteria("OICaf3")
        db.session.commit()
        r = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=1, status="pending")
        d = Dish.create_dish("DishOI3", "desc", 5.0, "main_course")
        db.session.commit()
        oi = OrderItem.create_order_item(reservation_id=r.reservation_id, dish_id=d.dish_id, quantity=2, is_takeaway=False, applied_price=5.0)
        db.session.commit()
        id_ = oi.item_id
        assert oi.delete_order_item()
        assert OrderItem.get_by_id(id_) is None
