import pytest
import requests

BASE_URL = "http://localhost:8081/api/v1"

ENDPOINTS = [
    # user_controller
    {"method": "GET", "url": f"{BASE_URL}/user/", "desc": "Liste users"},
    {"method": "GET", "url": f"{BASE_URL}/user/1", "desc": "Get user 1"},
    {"method": "POST", "url": f"{BASE_URL}/user/", "json": {"first_name": "x", "last_name": "x", "email": "a@b.c", "password": "1"}, "desc": "Création user"},
    {"method": "PUT", "url": f"{BASE_URL}/user/1", "json": {"first_name": "Modif"}, "desc": "Update user"},
    {"method": "DELETE", "url": f"{BASE_URL}/user/1", "desc": "Delete user"},
    {"method": "POST", "url": f"{BASE_URL}/user/balance", "json": {"amount": "10"}, "desc": "Ajout balance"},

    # cafeteria_controller
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/", "desc": "Liste cafétérias"},
    {"method": "GET", "url": f"{BASE_URL}/cafeteria/1", "desc": "Get cafétéria 1"},
    {"method": "POST", "url": f"{BASE_URL}/cafeteria/", "json": {"name": "Café Sans Auth"}, "desc": "Création cafétéria"},
    {"method": "PUT", "url": f"{BASE_URL}/cafeteria/1", "json": {"name": "Modif"}, "desc": "Update cafétéria"},
    {"method": "DELETE", "url": f"{BASE_URL}/cafeteria/1", "desc": "Delete cafétéria"},

    # dish_controller
    {"method": "GET", "url": f"{BASE_URL}/dish/", "desc": "Liste plats"},
    {"method": "GET", "url": f"{BASE_URL}/dish/1", "desc": "Get plat 1"},
    {"method": "POST", "url": f"{BASE_URL}/dish/", "json": {"name": "TestPlat", "description": "x", "dine_in_price": 1, "dish_type": "main_course"}, "desc": "Création plat"},
    {"method": "PUT", "url": f"{BASE_URL}/dish/1", "json": {"name": "PlatModifié"}, "desc": "Update plat"},
    {"method": "DELETE", "url": f"{BASE_URL}/dish/1", "desc": "Delete plat"},

    # daily_menu_controller
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/", "desc": "Liste menus"},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/1", "desc": "Get menu 1"},
    {"method": "GET", "url": f"{BASE_URL}/daily-menu/by-cafeteria/1", "desc": "Menu par cafétéria (auth!)"},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": "2025-01-01"}, "desc": "Création menu"},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu/1", "json": {"menu_date": "2025-01-02"}, "desc": "Update menu"},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu/1", "desc": "Delete menu"},

    # daily_menu_item_controller
    {"method": "GET", "url": f"{BASE_URL}/daily-menu-item/by-menu/1", "desc": "Liste items menu"},
    {"method": "POST", "url": f"{BASE_URL}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "desc": "Ajout item menu"},
    {"method": "PUT", "url": f"{BASE_URL}/daily-menu-item/1", "json": {"display_order": 2}, "desc": "Update item menu"},
    {"method": "DELETE", "url": f"{BASE_URL}/daily-menu-item/1", "desc": "Delete item menu"},

    # order_item_controller
    {"method": "GET", "url": f"{BASE_URL}/order-item/", "desc": "Liste order_items"},
    {"method": "GET", "url": f"{BASE_URL}/order-item/1", "desc": "Get order_item 1"},
    {"method": "DELETE", "url": f"{BASE_URL}/order-item/1", "desc": "Delete order_item"},

    # reservation_controller
    {"method": "GET", "url": f"{BASE_URL}/reservations/", "desc": "Liste reservations"},
    {"method": "POST", "url": f"{BASE_URL}/reservations/", "json": {"cafeteria_id": 1, "items": [{"dish_id": 1, "quantity": 1, "is_takeaway": False}]}, "desc": "Création réservation"},
    {"method": "GET", "url": f"{BASE_URL}/reservations/1", "desc": "Get réservation 1"},
    {"method": "PUT", "url": f"{BASE_URL}/reservations/1/cancel", "desc": "Cancel réservation"},
]

EXPECTED_UNAUTH = {401, 403}

@pytest.mark.parametrize("endpoint", ENDPOINTS, ids=[f"{ep['method']} {ep['url']} ({ep['desc']})" for ep in ENDPOINTS])
def test_api_auth_protection(endpoint):
    """
    Teste qu'une personne non authentifiée reçoit bien 401/403 sur les endpoints protégés.
    (Considère qu'absolument tous les endpoints API sont protégés sauf mention contraire)
    """
    try:
        resp = requests.request(
            method=endpoint["method"],
            url=endpoint["url"],
            json=endpoint.get("json"),
            timeout=5
        )
    except Exception as e:
        pytest.fail(f"Erreur lors de la requête HTTP: {e}")

    # Debug pour aider si le test échoue
    debug_info = f"URL: {endpoint['url']} | Code reçu: {resp.status_code}\nCorps: {resp.text[:150]}"
    assert resp.status_code in EXPECTED_UNAUTH, f"Le endpoint n'est PAS protégé correctement pour les non-authentifiés.\n{debug_info}"