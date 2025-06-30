import pytest
import requests

BASE_URL = "http://localhost:8081/api/v1"
LOGIN_URL = "http://localhost:8081/login"

# Utilisateur non-admin existant dans ton seeder :
USER_CREDENTIALS = {
    "username": "jakub.novak@example.com",
    "password": "pass123"
}

# Liste des endpoints avec l’attendu (autorisé ou interdit pour un user "normal").
ENDPOINTS = [
    # USERS
    {"method": "GET", "url": f"{BASE_URL}/user/", "desc": "Liste users", "allowed": False},
    {"method": "GET", "url": f"{BASE_URL}/user/3", "desc": "Voir ses infos", "allowed": True}, # user_id 3 = jakub.novak
    {"method": "GET", "url": f"{BASE_URL}/user/2", "desc": "Voir un autre user", "allowed": False},
    {"method": "POST", "url": f"{BASE_URL}/user/", "json": {"first_name": "x", "last_name": "x", "email": "y@b.c", "password": "1"}, "desc": "Création user", "allowed": False},
    {"method": "PUT", "url": f"{BASE_URL}/user/3", "json": {"first_name": "Modif"}, "desc": "Update soi-même", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/user/2", "json": {"first_name": "Hacker"}, "desc": "Update autre user", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/user/2", "desc": "Delete autre user", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/user/3", "desc": "Delete soi-même", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/user/balance", "json": {"amount": "10"}, "desc": "Ajout balance", "allowed": True},

    # CAFETERIA
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/", "desc": "Liste cafétérias", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/1", "desc": "Get cafétéria 1", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/cafeteria/", "json": {"name": "Café H4ck"}, "desc": "Création cafétéria", "allowed": False},
    {"method": "PUT", "url": f"{BASE_URL}/cafeteria/1", "json": {"name": "Modif"}, "desc": "Update cafétéria", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/cafeteria/1", "desc": "Delete cafétéria", "allowed": False},

    # DISHES
    {"method": "GET", "url": f"{BASE_URL}/dish/", "desc": "Liste plats", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/dish/1", "desc": "Get plat 1", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/dish/", "json": {"name": "TestPlat", "description": "x", "dine_in_price": 1, "dish_type": "main_course"}, "desc": "Création plat", "allowed": False},
    {"method": "PUT", "url": f"{BASE_URL}/dish/1", "json": {"name": "PlatModifié"}, "desc": "Update plat", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/dish/1", "desc": "Delete plat", "allowed": False},

    # DAILY MENU
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/", "desc": "Liste menus", "allowed": False},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/1", "desc": "Get menu 1", "allowed": False},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/by-cafeteria/1", "desc": "Menu par cafétéria (user)", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": "2025-01-01"}, "desc": "Création menu", "allowed": False},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu/1", "json": {"menu_date": "2025-01-02"}, "desc": "Update menu", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu/1", "desc": "Delete menu", "allowed": False},

    # DAILY MENU ITEM
    {"method": "GET", "url": f"{BASE_URL}/daily-menu-item/by-menu/1", "desc": "Liste items menu", "allowed": False},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "desc": "Ajout item menu", "allowed": False},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu-item/1", "json": {"display_order": 2}, "desc": "Update item menu", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu-item/1", "desc": "Delete item menu", "allowed": False},

    # ORDER ITEM
    {"method": "GET", "url": f"{BASE_URL}/order-item/", "desc": "Liste order_items", "allowed": False},
    {"method": "GET", "url": f"{BASE_URL}/order-item/1", "desc": "Get order_item 1", "allowed": False},
    {"method": "DELETE", "url": f"{BASE_URL}/order-item/1", "desc": "Delete order_item", "allowed": False},

    # RESERVATION
    {"method": "GET", "url": f"{BASE_URL}/reservations/", "desc": "Liste reservations", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/reservations/", "json": {"cafeteria_id": 1, "items": [{"dish_id": 1, "quantity": 1, "is_takeaway": False}]}, "desc": "Création réservation", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/reservations/1", "desc": "Get réservation 1", "allowed": False},  # Sauf si le user est propriétaire
    {"method": "PUT", "url": f"{BASE_URL}/reservations/1/cancel", "desc": "Cancel réservation", "allowed": False},  # Idem
]

@pytest.fixture(scope="session")
def user_session():
    """Se connecte en tant qu'user normal et récupère les cookies de session."""
    s = requests.Session()
    resp = s.post(LOGIN_URL, data=USER_CREDENTIALS, allow_redirects=False)
    # La connexion doit rediriger (302) si succès
    assert resp.status_code in (302, 303), f"Échec login user : {resp.status_code} {resp.text}"
    return s

@pytest.mark.parametrize(
    "endpoint", ENDPOINTS,
    ids=[f"{ep['method']} {ep['url']} ({ep['desc']})" for ep in ENDPOINTS]
)
def test_api_user_rights(endpoint, user_session):
    """
    Vérifie pour chaque endpoint si un user 'normal' y a accès ou non.
    """
    method = endpoint["method"]
    url = endpoint["url"]
    allowed = endpoint["allowed"]

    resp = user_session.request(
        method=method,
        url=url,
        json=endpoint.get("json"),
        timeout=5,
        allow_redirects=False
    )

    if allowed:
        assert resp.status_code in (200, 201, 204), f"[KO] Accès refusé à l'endpoint ALLOWED : {method} {url} ({resp.status_code})\n{resp.text[:300]}"
    else:
        assert resp.status_code in (401, 403), f"[KO] Endpoint réservé NON protégé : {method} {url} (code reçu: {resp.status_code})\n{resp.text[:300]}"
