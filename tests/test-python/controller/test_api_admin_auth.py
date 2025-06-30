import pytest
import requests

BASE_URL = "http://localhost:8081/api/v1"
LOGIN_URL = "http://localhost:8081/login"

ADMIN_CREDENTIALS = {
    "username": "admin@example.com",
    "password": "password"
}

ENDPOINTS = [
    # USERS
    {"method": "GET", "url": f"{BASE_URL}/user/", "desc": "Liste users", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/user/6", "desc": "Voir admin lui-même", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/user/2", "desc": "Voir autre user", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/user/", "json": {"first_name": "x", "last_name": "x", "email": "admin_add@b.c", "password": "1"}, "desc": "Création user", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/user/2", "json": {"first_name": "AdminUpdate"}, "desc": "Update autre user", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/user/2", "desc": "Delete autre user", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/user/6", "desc": "Delete soi-même (admin)", "allowed": False},
    {"method": "POST", "url": f"{BASE_URL}/user/balance", "json": {"amount": "10"}, "desc": "Ajout balance", "allowed": True},

    # CAFETERIA
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/", "desc": "Liste cafétérias", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/1", "desc": "Get cafétéria 1", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/cafeteria/", "json": {"name": "Café ADMIN"}, "desc": "Création cafétéria", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/cafeteria/1", "json": {"name": "ModifAdmin"}, "desc": "Update cafétéria", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/cafeteria/1", "desc": "Delete cafétéria", "allowed": True},

    # DISHES
    {"method": "GET", "url": f"{BASE_URL}/dish/", "desc": "Liste plats", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/dish/1", "desc": "Get plat 1", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/dish/", "json": {"name": "PlatADMIN", "description": "desc", "dine_in_price": 10, "dish_type": "main_course"}, "desc": "Création plat", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/dish/1", "json": {"name": "PlatADMIN_mod"}, "desc": "Update plat", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/dish/1", "desc": "Delete plat", "allowed": True},

    # DAILY MENU
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/", "desc": "Liste menus", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/1", "desc": "Get menu 1", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/by-cafeteria/1", "desc": "Menu par cafétéria", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": "2025-01-01"}, "desc": "Création menu", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu/1", "json": {"menu_date": "2025-01-02"}, "desc": "Update menu", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu/1", "desc": "Delete menu", "allowed": True},

    # DAILY MENU ITEM
    {"method": "GET", "url": f"{BASE_URL}/daily-menu-item/by-menu/1", "desc": "Liste items menu", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "desc": "Ajout item menu", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu-item/1", "json": {"display_order": 2}, "desc": "Update item menu", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu-item/1", "desc": "Delete item menu", "allowed": True},

    # ORDER ITEM
    {"method": "GET", "url": f"{BASE_URL}/order-item/", "desc": "Liste order_items", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/order-item/1", "desc": "Get order_item 1", "allowed": True},
    {"method": "DELETE", "url": f"{BASE_URL}/order-item/1", "desc": "Delete order_item", "allowed": True},

    # RESERVATION
    {"method": "GET", "url": f"{BASE_URL}/reservations/", "desc": "Liste reservations", "allowed": True},
    {"method": "POST", "url": f"{BASE_URL}/reservations/", "json": {"cafeteria_id": 1, "items": [{"dish_id": 1, "quantity": 1, "is_takeaway": False}]}, "desc": "Création réservation", "allowed": True},
    {"method": "GET", "url": f"{BASE_URL}/reservations/1", "desc": "Get réservation 1", "allowed": True},
    {"method": "PUT", "url": f"{BASE_URL}/reservations/1/cancel", "desc": "Cancel réservation", "allowed": True},
]

@pytest.fixture(scope="session")
def admin_session():
    """Se connecte en tant qu'admin et récupère les cookies de session."""
    s = requests.Session()
    resp = s.post(LOGIN_URL, data=ADMIN_CREDENTIALS, allow_redirects=False)
    assert resp.status_code in (302, 303), f"Échec login admin : {resp.status_code} {resp.text}"
    return s

@pytest.mark.parametrize(
    "endpoint", ENDPOINTS,
    ids=[f"{ep['method']} {ep['url']} ({ep['desc']})" for ep in ENDPOINTS]
)
def test_api_admin_rights(endpoint, admin_session):
    """
    Vérifie pour chaque endpoint si un admin a accès ou non.
    """
    method = endpoint["method"]
    url = endpoint["url"]
    allowed = endpoint["allowed"]

    resp = admin_session.request(
        method=method,
        url=url,
        json=endpoint.get("json"),
        timeout=5,
        allow_redirects=False
    )

    if allowed:
        assert resp.status_code in (200, 201, 204), f"[KO] Accès refusé à l'endpoint ALLOWED : {method} {url} ({resp.status_code})\n{resp.text[:300]}"
    else:
        assert resp.status_code in (401, 403), f"[KO] Endpoint interdit à l'admin NON protégé : {method} {url} (code reçu: {resp.status_code})\n{resp.text[:300]}"
