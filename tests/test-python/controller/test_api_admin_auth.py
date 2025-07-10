# tests/test-python/controller/test_api_admin_access.py

import pytest
import uuid

# Le préfixe de base pour toutes les routes de l'API v1
API_PREFIX = "/api/v1"

@pytest.fixture
def admin_client(client):
    """
    Fixture PyTest qui retourne un client de test authentifié en tant qu'administrateur.
    
    Cette fixture utilise le client de test Flask standard, effectue une requête POST
    sur la route /login avec les identifiants de l'admin, et vérifie que la connexion
    a réussi. Le client conserve le cookie de session pour les tests suivants.
    
    Args:
        client: La fixture de base du client de test Flask fournie par conftest.py.

    Yields:
        Le client de test Flask avec une session admin active.
    """
    admin_credentials = {
        "username": "admin@example.com",
        "password": "password"
    }
    # La route /login est une page web qui redirige. `follow_redirects=True`
    # permet de suivre la redirection vers le tableau de bord et de vérifier
    # que la connexion a bien fonctionné.
    response = client.post("/login", data=admin_credentials, follow_redirects=True)
    
    # Après une connexion réussie, on doit avoir un statut 200 et être sur le dashboard admin.
    assert response.status_code == 200, "La connexion de l'administrateur a échoué."
    # Vérifie un élément clé du tableau de bord admin pour confirmer la réussite.
    assert b"Admin Dashboard" in response.data, "La page de destination après le login ne semble pas être le dashboard admin."
    
    # Le 'client' a maintenant le cookie de session et est prêt pour les tests.
    yield client
    
    # Nettoyage : déconnexion à la fin des tests utilisant cette fixture.
    client.get("/logout")


# Génère une chaîne unique pour les tests de création afin d'éviter les conflits (409)
# si les tests sont exécutés plusieurs fois sans réinitialiser la base.
UNIQUE_ID = str(uuid.uuid4())[:8]

# Liste des endpoints qui doivent être accessibles par un administrateur.
# Chaque dictionnaire contient la méthode, l'URL, les données éventuelles (json)
# et le code de statut attendu pour une opération réussie.
ADMIN_ACCESSIBLE_ENDPOINTS = [
    # --- user_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/user/", "expected_status": 200, "desc": "Lister tous les utilisateurs"},
    {"method": "GET", "url": f"{API_PREFIX}/user/1", "expected_status": 200, "desc": "Récupérer un utilisateur par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/user/", "json": {"last_name": "Test", "first_name": "Admin", "email": f"test.admin.{UNIQUE_ID}@example.com", "password": "password"}, "expected_status": 201, "desc": "Créer un utilisateur"},
    {"method": "PUT", "url": f"{API_PREFIX}/user/1", "json": {"first_name": "StudentUpdated"}, "expected_status": 200, "desc": "Modifier un utilisateur"},
    # On ne teste pas la suppression d'utilisateurs/cafétérias de base pour ne pas casser d'autres tests.

    # --- cafeteria_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/cafeteria/", "expected_status": 200, "desc": "Lister les cafétérias"},
    {"method": "GET", "url": f"{API_PREFIX}/cafeteria/1", "expected_status": 200, "desc": "Récupérer une cafétéria par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/cafeteria/", "json": {"name": f"Café Test Admin {UNIQUE_ID}"}, "expected_status": 201, "desc": "Créer une cafétéria"},
    {"method": "PUT", "url": f"{API_PREFIX}/cafeteria/1", "json": {"name": "AR-Updated"}, "expected_status": 200, "desc": "Modifier une cafétéria"},

    # --- dish_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/dish/", "expected_status": 200, "desc": "Lister les plats"},
    {"method": "GET", "url": f"{API_PREFIX}/dish/1", "expected_status": 200, "desc": "Récupérer un plat par ID"},
    {"method": "POST", "url": f"{API_PREFIX}/dish/", "json": {"name": f"Plat Test Admin {UNIQUE_ID}", "description": "x", "dine_in_price": 1, "dish_type": "main_course"}, "expected_status": 201, "desc": "Créer un plat"},
    {"method": "PUT", "url": f"{API_PREFIX}/dish/1", "json": {"dine_in_price": 0.01}, "expected_status": 200, "desc": "Modifier un plat"},

    # --- daily_menu_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/", "expected_status": 200, "desc": "Lister tous les menus (admin)"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/1", "expected_status": 200, "desc": "Récupérer un menu par ID (admin)"},
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu/by-cafeteria/1", "params": {"date": "2025-06-30"}, "expected_status": 200, "desc": "Récupérer un menu par cafétéria (tout utilisateur auth)"},
    {"method": "POST", "url": f"{API_PREFIX}/daily-menu/", "json": {"cafeteria_id": 1, "menu_date": f"2099-12-{10 + int(UNIQUE_ID[:1], 16)}"}, "expected_status": 201, "desc": "Créer un menu (admin)"}, # Date unique pour éviter conflit

    # --- daily_menu_item_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/daily-menu-item/by-menu/1", "expected_status": 200, "desc": "Lister les items d'un menu (admin)"},
    {"method": "POST", "url": f"{API_PREFIX}/daily-menu-item/", "json": {"menu_id": 1, "dish_id": 1, "dish_role": "main_course"}, "expected_status": 201, "desc": "Ajouter un item à un menu (admin)"},

    # --- order_item_controller ---
    {"method": "GET", "url": f"{API_PREFIX}/order-item/", "expected_status": 200, "desc": "Lister les items de commande (admin)"},
]

@pytest.mark.parametrize(
    "endpoint",
    ADMIN_ACCESSIBLE_ENDPOINTS,
    # Génère des noms de tests plus lisibles
    ids=[f"{ep['method']}_{ep['url'].replace(API_PREFIX, '').replace('/', '_')}" for ep in ADMIN_ACCESSIBLE_ENDPOINTS]
)
def test_api_admin_access_is_granted(admin_client, endpoint):
    """
    Vérifie qu'un administrateur authentifié a bien accès aux endpoints protégés
    et que l'opération réussit avec le code de statut attendu.
    
    Args:
        admin_client: Le client de test authentifié en tant qu'admin.
        endpoint: Le dictionnaire décrivant l'endpoint à tester.
    """
    method = endpoint["method"].lower()
    url = endpoint["url"]
    
    # Récupère la méthode du client à appeler (get, post, put, delete)
    client_method_to_call = getattr(admin_client, method)
    
    # Prépare les arguments pour l'appel (json, data, params)
    kwargs = {}
    if "json" in endpoint:
        kwargs["json"] = endpoint.get("json")
    if "data" in endpoint:
        kwargs["data"] = endpoint.get("data")
    if "params" in endpoint:
        kwargs["query_string"] = endpoint.get("params")

    # Appelle la méthode du client de test
    response = client_method_to_call(url, **kwargs)

    # Informations de débogage en cas d'échec
    debug_info = (
        f"Endpoint: {endpoint['method']} {url}\n"
        f"Description: {endpoint['desc']}\n"
        f"Code de statut attendu: {endpoint['expected_status']}\n"
        f"Code de statut reçu: {response.status_code}\n"
        f"Corps de la réponse: {response.data.decode(errors='ignore')[:500]}"
    )

    assert response.status_code == endpoint['expected_status'], \
        f"L'accès admin a échoué ou retourné un code inattendu.\n{debug_info}"

def test_admin_can_get_existing_reservation_and_item(admin_client, app):
    """
    Vérifie qu'un admin peut récupérer une réservation et un order_item spécifiques.
    Ce test crée ses propres données pour garantir leur existence.
    
    Args:
        admin_client: Le client de test authentifié en tant qu'admin.
        app: La fixture de l'application Flask pour accéder au contexte.
    """
    # --- 1. SETUP : Création des données nécessaires ---
    with app.app_context():
        # Il est préférable d'importer les modèles ici pour éviter les dépendances circulaires
        from app.models import db, AppUser, Cafeteria, Dish, Reservation, OrderItem

        # On récupère des objets créés par le seeder de base (utilisateur, cafétéria, plat)
        user = db.session.get(AppUser, 1)
        cafeteria = db.session.get(Cafeteria, 1)
        dish = db.session.get(Dish, 1)

        # On s'assure que nos prérequis existent bien
        assert all([user, cafeteria, dish]), "Données de base (user, cafeteria, dish) manquantes du seeder."

        # On crée une nouvelle réservation
        reservation = Reservation(
            user_id=user.user_id,
            cafeteria_id=cafeteria.cafeteria_id,
            total=dish.dine_in_price
        )
        db.session.add(reservation)
        # db.session.flush() est crucial ici : il envoie les changements à la BDD
        # et assigne un ID à notre objet 'reservation' sans terminer la transaction.
        db.session.flush()

        # On crée un article de commande lié à cette réservation
        order_item = OrderItem(
            reservation_id=reservation.reservation_id,
            dish_id=dish.dish_id,
            quantity=1,
            applied_price=dish.dine_in_price,
            is_takeaway=False
        )
        db.session.add(order_item)
        db.session.commit() # On sauvegarde tout en base de données

        # On garde les ID pour les utiliser dans nos appels API
        reservation_id_to_test = reservation.reservation_id
        order_item_id_to_test = order_item.item_id

    # --- 2. TEST : On effectue les appels API avec les ID créés ---

    # Test sur la réservation
    response_reservation = admin_client.get(f"/api/v1/reservations/{reservation_id_to_test}")
    assert response_reservation.status_code == 200
    assert response_reservation.json['reservation_id'] == reservation_id_to_test
    print(f"\n✅ Test de la réservation {reservation_id_to_test} réussi.")

    # Test sur l'article de commande
    response_order_item = admin_client.get(f"/api/v1/order-item/{order_item_id_to_test}")
    assert response_order_item.status_code == 200
    assert response_order_item.json['item_id'] == order_item_id_to_test
    print(f"✅ Test de l'article de commande {order_item_id_to_test} réussi.")
