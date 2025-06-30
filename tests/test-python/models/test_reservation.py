# tests/test-python/models/test_reservation.py

from app.models.app_user import AppUser
from app.models.cafeteria import Cafeteria
from app.models.reservation import Reservation
from app.models import db
from datetime import datetime

def test_create_reservation(app):
    with app.app_context():
        user = AppUser.create_user("R", "Test", "rt@ex.com", "pw", "student")
        caf = Cafeteria.create_cafeteria("ResCaf")
        db.session.commit()
        r = Reservation.create_reservation(user_id=user.user_id, cafeteria_id=caf.cafeteria_id, total=12.34, status="pending")
        db.session.commit()
        assert r.reservation_id is not None

def test_update_reservation(app):
    with app.app_context():
        user = AppUser.create_user("RR", "TT", "rtt@ex.com", "pw", "student")
        caf = Cafeteria.create_cafeteria("RC2")
        db.session.commit()
        r = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=1, status="pending")
        db.session.commit()
        ok = r.update_reservation(total=99, status="completed")
        assert ok
        assert float(r.total) == 99
        assert r.status == "completed"

def test_delete_reservation(app):
    with app.app_context():
        user = AppUser.create_user("RRR", "TTT", "rrrttt@ex.com", "pw", "student")
        caf = Cafeteria.create_cafeteria("RC3")
        db.session.commit()
        r = Reservation.create_reservation(user.user_id, caf.cafeteria_id, total=1, status="pending")
        db.session.commit()
        id_ = r.reservation_id
        assert r.delete_reservation()
        assert Reservation.get_by_id(id_) is None
