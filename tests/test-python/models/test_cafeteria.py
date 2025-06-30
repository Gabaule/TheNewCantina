# tests/test-python/models/test_cafeteria.py

import pytest
from app.models.cafeteria import Cafeteria
from app.models import db

def test_create_cafeteria(app):
    with app.app_context():
        cafeteria = Cafeteria.create_cafeteria("Test Cafeteria")
        db.session.commit()
        assert cafeteria.cafeteria_id is not None
        assert cafeteria.name == "Test Cafeteria"
        assert Cafeteria.get_by_id(cafeteria.cafeteria_id) == cafeteria

def test_update_cafeteria(app):
    with app.app_context():
        cafeteria = Cafeteria.create_cafeteria("Old Name")
        db.session.commit()
        result = cafeteria.update_cafeteria(name="New Name")
        assert result
        assert cafeteria.name == "New Name"

def test_get_all_dicts(app):
    with app.app_context():
        Cafeteria.create_cafeteria("A")
        Cafeteria.create_cafeteria("B")
        db.session.commit()
        cafeterias = Cafeteria.get_all_dicts()
        assert isinstance(cafeterias, list)
        assert len(cafeterias) >= 2

def test_delete_cafeteria(app):
    with app.app_context():
        cafeteria = Cafeteria.create_cafeteria("To Delete")
        db.session.commit()
        id_ = cafeteria.cafeteria_id
        assert cafeteria.delete_cafeteria()
        assert Cafeteria.get_by_id(id_) is None
