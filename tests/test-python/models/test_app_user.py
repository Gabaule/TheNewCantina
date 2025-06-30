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

def test_app_user_update_nothing_returns_false(app):
    """Vérifie que appeler update_user sans arguments ne fait rien et renvoie False."""
    with app.app_context():
        user = AppUser.create_user("Test", "User", "coverage@test.com", "pass")
        db.session.commit()
        assert user.update_user() is False

def test_app_user_update_password_and_role(app):
    """Vérifie que la mise à jour du mot de passe et du rôle fonctionne."""
    with app.app_context():
        user = AppUser.create_user("Test", "User", "pw_role@test.com", "old_pass")
        db.session.commit()
        
        ok = user.update_user(password="new_pass", role="admin")
        assert ok is True
        assert user.role == "admin"
        assert user.verify_password("new_pass")
        assert not user.verify_password("old_pass")

def test_app_user_update_to_existing_email_fails(app):
    """Vérifie que la mise à jour vers un email existant échoue et renvoie False."""
    with app.app_context():
        AppUser.create_user("User", "One", "one@example.com", "p")
        user2 = AppUser.create_user("User", "Two", "two@example.com", "p")
        db.session.commit()
        
        ok = user2.update_user(email="one@example.com")
        assert ok is False

def test_app_user_get_all_dicts(app):
    """Teste la méthode utilitaire get_all_dicts."""
    with app.app_context():
        db.session.query(AppUser).delete()
        AppUser.create_user("A", "A", "a@a.com", "p")
        AppUser.create_user("B", "B", "b@b.com", "p")
        db.session.commit()
        users = AppUser.get_all_dicts()
        assert len(users) == 2
        assert users[0]['email'] == 'a@a.com'