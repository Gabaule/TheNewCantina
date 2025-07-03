# tests/test-python/controller/test_api_no_auth.py

import pytest

# Le BASE_URL et l'import 'requests' ne sont plus nécessaires.
# Nous utiliserons des chemins relatifs et le client de test Flask.
API_PREFIX = "/api/v1"

# La liste des endpoints est mise à jour avec des chemins relatifs.
ENDPOINTS = [
    # user_controller
    {"method": "GET", "url": f"{API_PREFIX}/user/", "desc": "Liste tous les utilisateurs"},
    {"method": "GET", "url": f"{API_PREFIX}/user/1", "desc": "Récupérer un utilisateur par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/user/", "json": {"first_name": "x", "last_name": "x", "email": "a@b.c", "password": "1"}, "desc": "Créer un utilisateur"},
    {"method": "PUT", "url": f"{API_PREFIX}/user/1", "json": {"first_name": "Modif"}, "desc": "Modifier un utilisateur"},
    {"method": "DELETE", "url": f"{API_PREFIX}/user/1", "desc": "Supprimer un utilisateur"},
    {"method": "POST", "url": f"{API_PREFIX}/user/balance", "json": {"amount": "10"}, "desc": "Ajouter de l'argent au solde"},

    # cafeteria_controller
    {"method": "GET", "url": f"{API_PREFIX}/cafeteria/", "desc": "Lister les cafétérias"},
    {"method": "GET", "url": f"{API_PREFIX}/cafeteria/1", "desc": "Récupérer une cafétéria par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/cafeteria/", "json": {"name": "Café Sans Auth"}, "desc": "Créer une cafétéria"},
    {"method": "PUT", "url": f"{API_PREFIX}/cafeteria/1", "json": {"name": "Modif"}, "desc": "Modifier une cafétéria"},
    {"method": "DELETE", "url": f"{API_PREFIX}/cafeteria/1", "desc": "Supprimer une cafétéria"},

    # dish_controller
    {"method": "GET", "url": f"{API_PREFIX}/dish/", "desc": "Lister les plats"},
    {"method": "GET", "url": f"{API_PREFIX}/dish/1", "desc": "Récupérer un plat par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/dish/", "json": {"name": "TestPlat", "description": "x", "dine_in_price": 1, "dish_type": "main_course"}, "desc": "Créer un plat"},
    {"method": "PUT", "url": f"{API_PREFIX}/dish/1", "json": {"name": "PlatModifié"}, "desc": "Modifier un plat"},
    {"method": "DELETE", "url": f"{API_PREFIX}/dish/1", "desc": "Supprimer un plat"},

    # daily_menu_controller
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/", "desc": "Lister tous les menus"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/1", "desc": "Récupérer un menu par ID"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/by-cafeteria/1", "desc": "Récupérer un menu par cafétéria"},
    {"method": "POST", "url": f"{API_PREFIX}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": "2025-01-01"}, "desc": "Créer un menu"},
    {"method": "PUT", "url": f"{API_PREFIX}/daily-menu/1", "json": {"menu_date": "2025-01-02"}, "desc": "Modifier un menu"},
    {"method": "DELETE", "url": f"{API_PREFIX}/daily-menu/1", "desc": "Supprimer un menu"},

    # daily_menu_item_controller
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu-item/by-menu/1", "desc": "Lister les items d'un menu"},
    {"method": "POST", "url": f"{API_PREFIX}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "desc": "Ajouter un item à un menu"},
    {"method": "PUT", "url": f"{API_PREFIX}/daily-menu-item/1", "json": {"display_order": 2}, "desc": "Modifier un item de menu"},
    {"method": "DELETE", "url": f"{API_PREFIX}/daily-menu-item/1", "desc": "Supprimer un item de menu"},

    # order_item_controller
    {"method": "GET", "url": f"{API_PREFIX}/order-item/", "desc": "Lister les items de commande"},
    {"method": "GET", "url": f"{API_PREFIX}/order-item/1", "desc": "Récupérer un item de commande par ID"},
    {"method": "DELETE", "url": f"{API_PREFIX}/order-item/1", "desc": "Supprimer un item de commande"},

    # reservation_controller
    {"method": "GET", "url": f"{API_PREFIX}/reservations/", "desc": "Lister les réservations"},
    {"method": "POST", "url": f"{API_PREFIX}/reservations/", "json": {"cafeteria_id": 1, "items": [{"dish_id": 1, "quantity": 1, "is_takeaway": False}]}, "desc": "Créer une réservation"},
    {"method": "GET", "url": f"{API_PREFIX}/reservations/1", "desc": "Récupérer une réservation par ID"},
    {"method": "PUT", "url": f"{API_PREFIX}/reservations/1/cancel", "desc": "Annuler une réservation"},
]

# Les codes d'erreur attendus pour un utilisateur non authentifié sont 401 (Unauthorized) ou 403 (Forbidden)
EXPECTED_UNAUTH_STATUS_CODES = {401, 403}

@pytest.mark.parametrize(
    "endpoint",
    ENDPOINTS,
    # Génère des noms de tests plus lisibles dans le rapport pytest
    ids=[f"{ep['method']}_{ep['url'].replace(API_PREFIX, '').replace('/', '_')}_({ep['desc']})" for ep in ENDPOINTS]
)
def test_api_unauthenticated_access_is_denied(client, endpoint):
    """
    Vérifie qu'un client non authentifié est bien rejeté des endpoints protégés.
    Le 'client' est la fixture du test_client de Flask venant de conftest.py.
    """
    method = endpoint["method"].lower()
    url = endpoint["url"]
    
    # Récupère dynamiquement la méthode du client (client.get, client.post, etc.)
    client_method_to_call = getattr(client, method)
    
    # Prépare les arguments pour l'appel (json ou data)
    kwargs = {}
    if "json" in endpoint:
        kwargs["json"] = endpoint.get("json")

    # Appelle la méthode du client de test
    response = client_method_to_call(url, **kwargs)

    # Informations de débogage en cas d'échec du test
    debug_info = (
        f"Endpoint: {endpoint['method']} {url}\n"
        f"Description: {endpoint['desc']}\n"
        f"Code de statut reçu: {response.status_code}\n"
        f"Corps de la réponse: {response.data.decode(errors='ignore')[:200]}"
    )

    assert response.status_code in EXPECTED_UNAUTH_STATUS_CODES, \
        f"L'accès non authentifié a été AUTORISÉ alors qu'il devrait être refusé.\n{debug_info}"