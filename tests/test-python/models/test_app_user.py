from app.models.app_user import AppUser
from app.models import db

def test_create_user(app):
    with app.app_context():
        user = AppUser.create_user(
            last_name="Test",
            first_name="User",
            email="testuser@example.com",
            password="secret",
            role="student",
            balance=10.00
        )
        db.session.commit()
        assert user.user_id is not None
        assert user.email == "testuser@example.com"
        assert user.password != "secret"
        assert user.verify_password("secret")
        assert not user.verify_password("wrongpass")

def test_update_user(app):
    with app.app_context():
        user = AppUser.create_user(
            last_name="Foo",
            first_name="Bar",
            email="foo@bar.com",
            password="foobar",
            role="student"
        )
        db.session.commit()
        user.update_user(last_name="Baz", balance=42)
        assert user.last_name == "Baz"
        assert float(user.balance) == 42

def test_unique_email_constraint(app):
    with app.app_context():
        u1 = AppUser.create_user("A", "B", "dup@ex.com", "x", "student")
        db.session.commit()
        u2 = AppUser.create_user("C", "D", "dup@ex.com", "y", "student")
        try:
            db.session.commit()
            assert False, "Should fail on duplicate email"
        except Exception:
            db.session.rollback()

def test_delete_user(app):
    with app.app_context():
        user = AppUser.create_user(
            last_name="Delete",
            first_name="Me",
            email="deleteme@example.com",
            password="deleteme"
        )
        db.session.commit()
        user_id = user.user_id
        assert AppUser.get_by_id(user_id)
        user.delete_user()
        assert AppUser.get_by_id(user_id) is None
