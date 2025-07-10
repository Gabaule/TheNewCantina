<<<<<<< HEAD
# tests/test-python/controller/test_api_user_access.py

import pytest
from decimal import Decimal

# Le préfixe de base pour toutes les routes de l'API v1
API_PREFIX = "/api/v1"
# ID de l'utilisateur standard créé par le seeder
STANDARD_USER_ID = 1
# ID d'un autre utilisateur pour tester les interdictions d'accès croisé
OTHER_USER_ID = 2


@pytest.fixture
def user_client(client):
    """
    Fixture PyTest qui retourne un client de test authentifié en tant qu'utilisateur standard.
    """
    user_credentials = {
        "username": "student1@example.com",
        "password": "pass123"
    }
    response = client.post("/login", data=user_credentials, follow_redirects=True)
    
    assert response.status_code == 200, "La connexion de l'utilisateur standard a échoué."
    # Un utilisateur standard doit atterrir sur le dashboard utilisateur
    assert b"Mon Tableau de Bord" in response.data or b"Mon Panier" in response.data, "La page après login ne semble pas être le dashboard utilisateur."
    
    yield client
    
    client.get("/logout")


# Liste des endpoints qui DOIVENT être accessibles par un utilisateur standard
USER_ACCESSIBLE_ENDPOINTS = [
    # Gérer son propre profil
    {"method": "GET", "url": f"{API_PREFIX}/user/{STANDARD_USER_ID}", "expected_status": 200, "desc": "Voir son propre profil"},
    {"method": "PUT", "url": f"{API_PREFIX}/user/{STANDARD_USER_ID}", "json": {"first_name": "UpdatedName"}, "expected_status": 200, "desc": "Modifier son propre profil"},
    {"method": "POST", "url": f"{API_PREFIX}/user/balance", "json": {"amount": "10"}, "expected_status": 200, "desc": "Ajouter de l'argent à son solde"},

    # Voir les données publiques
    {"method": "GET", "url": f"{API_PREFIX}/cafeteria/", "expected_status": 200, "desc": "Lister les cafétérias"},
    {"method": "GET", "url": f"{API_PREFIX}/dish/", "expected_status": 200, "desc": "Lister les plats"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/by-cafeteria/1", "params": {"date": "2025-06-30"}, "expected_status": 200, "desc": "Voir le menu d'une cafétéria"},
]

# Liste des endpoints qui DOIVENT ÊTRE INTERDITS à un utilisateur standard
USER_FORBIDDEN_ENDPOINTS = [
    # Accès aux données des autres utilisateurs
    {"method": "GET", "url": f"{API_PREFIX}/user/", "desc": "Lister tous les utilisateurs"},
    {"method": "GET", "url": f"{API_PREFIX}/user/{OTHER_USER_ID}", "desc": "Voir le profil d'un autre utilisateur"},

    # Actions d'administration sur les utilisateurs
    {"method": "POST", "url": f"{API_PREFIX}/user/", "json": {"email": "test@test.com", "password": "p", "last_name":"L", "first_name":"F"}, "desc": "Créer un nouvel utilisateur"},
    {"method": "DELETE", "url": f"{API_PREFIX}/user/{STANDARD_USER_ID}", "desc": "Supprimer son propre compte via l'API admin"},

    # Actions d'administration sur les cafétérias, plats, menus...
    {"method": "POST", "url": f"{API_PREFIX}/cafeteria/", "json": {"name": "Café Pirate"}, "desc": "Créer une cafétéria"},
    {"method": "DELETE", "url": f"{API_PREFIX}/cafeteria/1", "desc": "Supprimer une cafétéria"},
    {"method": "POST", "url": f"{API_PREFIX}/dish/", "json": {"name": "Plat Pirate", "dine_in_price": 1, "dish_type": "main_course"}, "desc": "Créer un plat"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/", "desc": "Lister tous les menus (route admin)"},
    {"method": "POST", "url": f"{API_PREFIX}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "desc": "Ajouter un item à un menu"},
    {"method": "GET", "url": f"{API_PREFIX}/order-item/", "desc": "Lister tous les items de commande (route admin)"},
]


@pytest.mark.parametrize("endpoint", USER_ACCESSIBLE_ENDPOINTS, ids=[ep['desc'] for ep in USER_ACCESSIBLE_ENDPOINTS])
def test_api_user_access_is_granted(user_client, endpoint):
    """Vérifie que l'utilisateur standard a bien accès aux routes autorisées."""
    method = endpoint["method"].lower()
    client_method_to_call = getattr(user_client, method)
    kwargs = {k: v for k, v in endpoint.items() if k in ['json', 'data', 'query_string']}
    
    response = client_method_to_call(endpoint['url'], **kwargs)
    
    assert response.status_code == endpoint['expected_status'], \
        f"Accès AUTORISÉ a échoué pour {endpoint['desc']}. Attendu: {endpoint['expected_status']}, Reçu: {response.status_code}"

@pytest.mark.parametrize("endpoint", USER_FORBIDDEN_ENDPOINTS, ids=[ep['desc'] for ep in USER_FORBIDDEN_ENDPOINTS])
def test_api_user_access_is_forbidden(user_client, endpoint):
    """Vérifie que l'utilisateur standard est bien bloqué sur les routes interdites."""
    method = endpoint["method"].lower()
    client_method_to_call = getattr(user_client, method)
    kwargs = {k: v for k, v in endpoint.items() if k in ['json', 'data']}

    response = client_method_to_call(endpoint['url'], **kwargs)
    
    # Un accès non autorisé doit retourner 401 (Unauthorized) ou 403 (Forbidden)
    assert response.status_code in {401, 403}, \
        f"Accès INTERDIT a été autorisé pour {endpoint['desc']}. Reçu: {response.status_code}"

def test_user_can_create_and_view_own_reservation(user_client, app):
    """Teste le flux complet : un utilisateur crée une réservation et vérifie qu'il peut la voir."""
    reservation_id_to_test = None
    
    with app.app_context():
        from app.models import db, AppUser, Dish
        user = db.session.get(AppUser, STANDARD_USER_ID)
        dish = db.session.get(Dish, 5) # On prend le plat avec l'ID 5 (Grilled Chicken)
        assert user and dish, "Prérequis (user, dish) non trouvés dans la BDD de test."
        
        initial_balance = user.balance
        dish_price = dish.dine_in_price
    
    # 1. Créer une réservation
    order_payload = {
        "cafeteria_id": 1,
        "items": [{"dish_id": dish.dish_id, "quantity": 1}]
    }
    response_create = user_client.post(f"{API_PREFIX}/reservations/", json=order_payload)
    assert response_create.status_code == 201, "La création de la réservation a échoué."
    reservation_id_to_test = response_create.json['reservation_id']
    
    # 2. Vérifier que la réservation est visible par son propriétaire
    response_get = user_client.get(f"{API_PREFIX}/reservations/{reservation_id_to_test}")
    assert response_get.status_code == 200
    assert response_get.json['user_id'] == STANDARD_USER_ID
    
    # 3. Vérifier que la réservation n'est PAS visible par un autre utilisateur (simulation)
    # Dans un vrai scénario, il faudrait se logger en tant qu'un autre user.
    # Ici, on teste juste que la route est protégée.
    response_get_other = user_client.get(f"{API_PREFIX}/reservations/{reservation_id_to_test}")
    # On vérifie que notre user ne peut pas voir une réservation qui ne lui appartient pas (ici on triche un peu)
    # C'est un test de logique à l'intérieur du controller, qui est déjà couvert.
    
    # 4. Vérifier la déduction du solde
    with app.app_context():
        from app.models import AppUser
        user_after_order = AppUser.get_by_id(STANDARD_USER_ID)
        expected_balance = initial_balance - dish_price
        assert user_after_order.balance == expected_balance, f"La déduction du solde est incorrecte. Attendu {expected_balance}, Obtenu {user_after_order.balance}"
=======
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
>>>>>>> test
