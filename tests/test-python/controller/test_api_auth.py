# tests/test-python/controller/test_api_auth.py

import pytest
from app.models import db, AppUser, Reservation

API_PREFIX = "/api/v1"

@pytest.fixture
def authenticated_client(client):
    """
    Fixture qui connecte l'utilisateur standard 'jakub.novak@example.com' 
    (créé par le seeder) et retourne le client authentifié.
    """
    credentials = {
        "username": "jakub.novak@example.com",
        "password": "pass123"
    }
    response = client.post('/login', data=credentials, follow_redirects=True)
    assert response.status_code == 200, "La connexion de l'utilisateur a échoué."
    
    yield client # Le client conserve le cookie de session pour les tests
    
    client.get('/logout') # Déconnexion après chaque test


# Liste des endpoints à tester pour un utilisateur NON-ADMIN
# On utilise des placeholders {id} qui seront remplacés dans le test.
ENDPOINTS_PERMISSIONS = [
    # --- Requêtes ADMIN (devraient toutes être refusées) ---
    {"method": "GET",    "url": f"{API_PREFIX}/user/", "allowed": False, "desc": "Lister tous les utilisateurs"},
    {"method": "POST",   "url": f"{API_PREFIX}/user/", "json": {"email": "new@user.com"}, "allowed": False, "desc": "Créer un utilisateur"},
    {"method": "PUT",    "url": f"{API_PREFIX}/user/{{other_user_id}}", "json": {"first_name": "Hack"}, "allowed": False, "desc": "Modifier un autre utilisateur"},
    {"method": "DELETE", "url": f"{API_PREFIX}/user/{{other_user_id}}", "allowed": False, "desc": "Supprimer un autre utilisateur"},
    {"method": "POST",   "url": f"{API_PREFIX}/cafeteria/", "json": {"name": "Test Cafe"}, "allowed": False, "desc": "Créer une cafétéria"},
    {"method": "POST",   "url": f"{API_PREFIX}/dish/", "json": {"name": "Test Dish", "dine_in_price": 1, "dish_type": "soup"}, "allowed": False, "desc": "Créer un plat"},
    {"method": "POST",   "url": f"{API_PREFIX}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": "2030-01-01"}, "allowed": False, "desc": "Créer un menu"},

    # --- Requêtes sur ses propres données (devraient être autorisées) ---
    {"method": "GET",    "url": f"{API_PREFIX}/user/{{current_user_id}}", "allowed": True, "desc": "Voir ses propres informations"},
    {"method": "PUT",    "url": f"{API_PREFIX}/user/{{current_user_id}}", "json": {"first_name": "Jakub Modif"}, "allowed": True, "desc": "Modifier ses propres informations"},
    {"method": "POST",   "url": f"{API_PREFIX}/user/balance", "json": {"amount": "5"}, "allowed": True, "desc": "Ajouter à son propre solde"},
    {"method": "GET",    "url": f"{API_PREFIX}/reservations/", "allowed": True, "desc": "Voir ses propres réservations"},
    {"method": "POST",   "url": f"{API_PREFIX}/reservations/", "json": {"cafeteria_id": 1, "items": [{"dish_id": 1, "quantity": 1}]}, "allowed": True, "desc": "Créer une réservation"},
    
    # --- Requêtes sur les données d'autres utilisateurs (devraient être refusées) ---
    {"method": "GET",    "url": f"{API_PREFIX}/user/{{other_user_id}}", "allowed": False, "desc": "Voir les infos d'un autre utilisateur"},
    {"method": "GET",    "url": f"{API_PREFIX}/reservations/{{other_user_reservation_id}}", "allowed": False, "desc": "Voir la réservation d'un autre"},
    {"method": "PUT",    "url": f"{API_PREFIX}/reservations/{{other_user_reservation_id}}/cancel", "allowed": False, "desc": "Annuler la réservation d'un autre"},
]

@pytest.mark.parametrize("endpoint_config", ENDPOINTS_PERMISSIONS)
def test_user_api_permissions(authenticated_client, endpoint_config):
    """
    Teste systématiquement les permissions d'un utilisateur standard connecté.
    """
    client = authenticated_client
    
    with client.application.app_context():
        # Récupère les objets depuis la BDD (créés par le seeder)
        current_user = AppUser.get_by_email("jakub.novak@example.com")
        other_user = AppUser.get_by_email("john.smith@example.com")
        
        # Crée une réservation pour 'l'autre utilisateur' si nécessaire pour le test
        other_reservation = Reservation(user_id=other_user.user_id, cafeteria_id=1, total=1.0)
        db.session.add(other_reservation)
        db.session.flush() # Utilise flush pour obtenir l'ID sans commit

        # Prépare l'URL finale en injectant les IDs
        url = endpoint_config["url"].format(
            current_user_id=current_user.user_id,
            other_user_id=other_user.user_id,
            other_user_reservation_id=other_reservation.reservation_id
        )

    # Exécute la requête de test
    method = endpoint_config["method"].lower()
    kwargs = {"json": endpoint_config.get("json")} if "json" in endpoint_config else {}
    response = getattr(client, method)(url, **kwargs)

    # Vérifie le code de statut
    allowed = endpoint_config["allowed"]
    debug_info = (
        f"Endpoint: {endpoint_config['method']} {url}\n"
        f"Description: {endpoint_config['desc']}\n"
        f"Attendu: {'Autorisé (2xx)' if allowed else 'Refusé (401/403)'}\n"
        f"Reçu: {response.status_code}\n"
        f"Réponse: {response.data.decode(errors='ignore')[:200]}"
    )
    
    if allowed:
        assert 200 <= response.status_code < 300, f"Accès REFUSÉ à un endpoint qui devait être autorisé.\n{debug_info}"
    else:
        assert response.status_code in {401, 403}, f"Accès AUTORISÉ à un endpoint qui devait être refusé.\n{debug_info}"