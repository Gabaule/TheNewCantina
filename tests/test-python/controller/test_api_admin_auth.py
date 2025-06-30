# test_admin_api.py
import pytest
import requests
from datetime import date, timedelta

# --- CONFIGURATION ---
BASE_URL = "http://localhost:8081"
API_PREFIX = "/api/v1"
ADMIN_CREDENTIALS = {
    "username": "admin@example.com",
    "password": "password"
}

@pytest.fixture(scope="session")
def admin_session():
    """
    Fixture Pytest pour s'authentifier une seule fois pour toute la session de test.
    Ceci est beaucoup plus efficace que de se logger avant chaque test.
    """
    print("\n--- (Setup Fixture) Authentification Administrateur ---")
    s = requests.Session()
    login_url = f"{BASE_URL}/login"
    
    response = s.post(login_url, data=ADMIN_CREDENTIALS, timeout=5)
    
    # Vérification robuste de la réussite du login
    assert response.status_code == 200, "Le login a retourné un code d'erreur"
    assert "session" in s.cookies, "Le cookie de session est manquant après le login."
    # Vérifie que la réponse finale (après redirection) contient un élément attendu du dashboard
    assert "admin/dashboard" in response.url or "Dashboard" in response.text, "La page après login ne semble pas être le dashboard."
    
    print("--- Authentification réussie. Début des tests. ---")
    yield s
    # Ici, on pourrait ajouter du code de "teardown" (nettoyage) si nécessaire,
    # comme un appel à /logout.
    print("\n--- Fin de la session de test. ---")


def test_user_crud(admin_session):
    """Teste les opérations CRUD complètes sur les endpoints utilisateur."""
    print("\n--- Test des Endpoints: Utilisateurs (User) ---")
    user_data = {
        "last_name": "TestPytest",
        "first_name": "Utilisateur",
        "email": f"test.user.pytest.{date.today()}@example.com", # Email unique
        "password": "password123",
        "role": "student",
        "balance": 20.0
    }
    user_id = None
    try:
        # 1. CREATE
        res = admin_session.post(f"{BASE_URL}{API_PREFIX}/user/", json=user_data)
        assert res.status_code == 201, f"CREATE User a échoué: {res.text}"
        user_id = res.json()['user_id']
        print(f"  ✅ CREATE User (ID: {user_id})")

        # 2. READ (List)
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/user/")
        assert res.status_code == 200
        assert any(u['user_id'] == user_id for u in res.json()), "Utilisateur créé non trouvé dans la liste"
        print("  ✅ READ User List")

        # 3. READ (Single)
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/user/{user_id}")
        assert res.status_code == 200
        assert res.json()['email'] == user_data['email']
        print("  ✅ READ Single User")

        # 4. UPDATE
        update_data = {"last_name": "TestModifié", "role": "staff"}
        res = admin_session.put(f"{BASE_URL}{API_PREFIX}/user/{user_id}", json=update_data)
        assert res.status_code == 200
        assert res.json()['last_name'] == "TestModifié"
        print("  ✅ UPDATE User")

    finally:
        # 5. DELETE (Cleanup)
        if user_id:
            res = admin_session.delete(f"{BASE_URL}{API_PREFIX}/user/{user_id}")
            assert res.status_code == 200, "Le nettoyage de l'utilisateur a échoué"
            print("  ✅ DELETE User (Cleanup)")

def test_cafeteria_crud(admin_session):
    """Teste les opérations CRUD complètes sur les endpoints cafétéria."""
    print("\n--- Test des Endpoints: Cafétérias (Cafeteria) ---")
    cafeteria_data = {"name": "Cafeteria de Test Pytest"}
    cafeteria_id = None
    try:
        # 1. CREATE
        res = admin_session.post(f"{BASE_URL}{API_PREFIX}/cafeteria/", json=cafeteria_data)
        assert res.status_code == 201
        cafeteria_id = res.json()['cafeteria_id']
        print(f"  ✅ CREATE Cafeteria (ID: {cafeteria_id})")

        # 2. READ (List & Single)
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/cafeteria/")
        assert res.status_code == 200
        assert any(c['cafeteria_id'] == cafeteria_id for c in res.json())
        print("  ✅ READ Cafeteria List")

        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/cafeteria/{cafeteria_id}")
        assert res.status_code == 200
        print("  ✅ READ Single Cafeteria")

        # 3. UPDATE
        res = admin_session.put(f"{BASE_URL}{API_PREFIX}/cafeteria/{cafeteria_id}", json={"name": "Nouveau Nom Café Pytest"})
        assert res.status_code == 200
        assert res.json()['name'] == "Nouveau Nom Café Pytest"
        print("  ✅ UPDATE Cafeteria")

    finally:
        # 4. DELETE
        if cafeteria_id:
            res = admin_session.delete(f"{BASE_URL}{API_PREFIX}/cafeteria/{cafeteria_id}")
            assert res.status_code == 200
            print("  ✅ DELETE Cafeteria (Cleanup)")

def test_dish_crud(admin_session):
    """Teste les opérations CRUD complètes sur les endpoints plat."""
    print("\n--- Test des Endpoints: Plats (Dish) ---")
    dish_data = {"name": "Plat de Test Pytest", "description": "Un plat pour pytest.", "dine_in_price": 9.99, "dish_type": "main_course"}
    dish_id = None
    try:
        # 1. CREATE
        print("  - Étape 1: Création du plat...")
        res_create = admin_session.post(f"{BASE_URL}{API_PREFIX}/dish/", json=dish_data)
        assert res_create.status_code == 201, f"CREATE Dish a échoué: {res_create.text}"
        created_dish = res_create.json()
        dish_id = created_dish.get('dish_id')
        assert dish_id is not None, "La réponse de création ne contient pas de 'dish_id'"
        print(f"  ✅ CREATE Dish (ID: {dish_id})")

        # --- AJOUT DE VÉRIFICATION IMMÉDIATE ---
        # Essayons de relire le plat par son ID immédiatement pour voir s'il existe.
        print(f"  - Vérification immédiate: Lecture du plat {dish_id}...")
        res_read_single = admin_session.get(f"{BASE_URL}{API_PREFIX}/dish/{dish_id}")
        assert res_read_single.status_code == 200, f"READ Single Dish a échoué juste après la création pour l'ID {dish_id}: {res_read_single.text}"
        print("  ✅ Le plat est lisible individuellement.")
        
        # 2. READ (List)
        print("  - Étape 2: Lecture de la liste complète des plats...")
        res_list = admin_session.get(f"{BASE_URL}{API_PREFIX}/dish/")
        assert res_list.status_code == 200, f"READ Dish List a retourné un code d'erreur: {res_list.text}"
        
        all_dishes = res_list.json()
        
        # --- DÉBOGAGE : AFFICHONS LES DONNÉES ---
        print(f"  - ID du plat recherché: {dish_id} (type: {type(dish_id)})")
        print(f"  - Nombre de plats reçus dans la liste: {len(all_dishes)}")
        print(f"  - IDs des 5 premiers plats reçus: {[d.get('dish_id') for d in all_dishes[:5]]}")

        # La vérification
        is_found = any(d.get('dish_id') == dish_id for d in all_dishes)
        
        if not is_found:
            # Si non trouvé, affichons la liste complète pour comprendre pourquoi
            import json
            print("--- ERREUR: Plat non trouvé dans la liste. Contenu de la liste reçue: ---")
            print(json.dumps(all_dishes, indent=2))
            print("----------------------------------------------------------------------")

        assert is_found, f"Le plat créé (ID: {dish_id}) est introuvable dans la liste des plats retournée par l'API."
        print("  ✅ READ Dish List")

        # 3. UPDATE
        print("  - Étape 3: Mise à jour du plat...")
        res_update = admin_session.put(f"{BASE_URL}{API_PREFIX}/dish/{dish_id}", json={"dine_in_price": 12.50})
        assert res_update.status_code == 200 and res_update.json()['dine_in_price'] == 12.50
        print("  ✅ UPDATE Dish")

    finally:
        # 4. DELETE (Cleanup)
        if dish_id:
            print(f"  - Étape 4: Nettoyage du plat (ID: {dish_id})...")
            res_delete = admin_session.delete(f"{BASE_URL}{API_PREFIX}/dish/{dish_id}")
            assert res_delete.status_code == 200, f"Le nettoyage du plat a échoué: {res_delete.text}"
            print("  ✅ DELETE Dish (Cleanup)")


def test_menu_and_item_crud(admin_session):
    """Teste les endpoints pour les menus et leurs items, en gérant les dépendances."""
    print("\n--- Test des Endpoints: Menus (DailyMenu & DailyMenuItem) ---")
    cafeteria_id, dish_id, menu_id, item_id = None, None, None, None
    try:
        # --- Prérequis ---
        res_caf = admin_session.post(f"{BASE_URL}{API_PREFIX}/cafeteria/", json={"name": "Café pour Menu Pytest"})
        assert res_caf.status_code == 201
        cafeteria_id = res_caf.json()['cafeteria_id']
        print(f"  ➡️ Prérequis: Création cafétéria (ID: {cafeteria_id})")

        res_dish = admin_session.post(f"{BASE_URL}{API_PREFIX}/dish/", json={"name": "Plat pour Menu Pytest", "dine_in_price": 5, "dish_type": "soup"})
        assert res_dish.status_code == 201
        dish_id = res_dish.json()['dish_id']
        print(f"  ➡️ Prérequis: Création plat (ID: {dish_id})")
        
        # --- Tests DailyMenu ---
        menu_date = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')
        res = admin_session.post(f"{BASE_URL}{API_PREFIX}/daily-menu/", json={"cafeteria_id": cafeteria_id, "menu_date": menu_date})
        assert res.status_code == 201
        menu_id = res.json()['menu_id']
        print(f"  ✅ CREATE DailyMenu (ID: {menu_id})")

        # --- Tests DailyMenuItem ---
        item_data = {"menu_id": menu_id, "dish_id": dish_id, "dish_role": "soup", "display_order": 1}
        res = admin_session.post(f"{BASE_URL}{API_PREFIX}/daily-menu-item/", json=item_data)
        assert res.status_code == 201
        item_id = res.json()['menu_item_id']
        print(f"  ✅ CREATE DailyMenuItem (ID: {item_id})")

        # --- Vérifications ---
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/daily-menu-item/by-menu/{menu_id}")
        assert res.status_code == 200 and any(i['menu_item_id'] == item_id for i in res.json())
        print("  ✅ READ MenuItem List")
        
    finally:
        # --- Nettoyage dans l'ordre inverse des dépendances ---
        if item_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/daily-menu-item/{item_id}")
            print(f"  🧹 Cleanup: DELETE DailyMenuItem ({item_id})")
        if menu_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/daily-menu/{menu_id}")
            print(f"  🧹 Cleanup: DELETE DailyMenu ({menu_id})")
        if dish_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/dish/{dish_id}")
            print(f"  🧹 Cleanup: DELETE Dish ({dish_id})")
        if cafeteria_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/cafeteria/{cafeteria_id}")
            print(f"  🧹 Cleanup: DELETE Cafeteria ({cafeteria_id})")

def test_reservation_and_order_item_flow(admin_session):
    """Teste le flux de réservation, qui crée implicitement des OrderItems."""
    print("\n--- Test des Endpoints: Réservations (Reservation & OrderItem) ---")
    cafeteria_id, dish_id = None, None
    try:
        # --- Prérequis ---
        res_caf = admin_session.post(f"{BASE_URL}{API_PREFIX}/cafeteria/", json={"name": "Café pour Commande Pytest"})
        assert res_caf.status_code == 201
        cafeteria_id = res_caf.json()['cafeteria_id']
        print(f"  ➡️ Prérequis: Création cafétéria (ID: {cafeteria_id})")

        res_dish = admin_session.post(f"{BASE_URL}{API_PREFIX}/dish/", json={"name": "Plat à commander Pytest", "dine_in_price": 7.50, "dish_type": "main_course"})
        assert res_dish.status_code == 201
        dish_id = res_dish.json()['dish_id']
        print(f"  ➡️ Prérequis: Création plat (ID: {dish_id})")
        
        # 1. CREATE Reservation
        reservation_data = {"cafeteria_id": cafeteria_id, "items": [{"dish_id": dish_id, "quantity": 2}]}
        res = admin_session.post(f"{BASE_URL}{API_PREFIX}/reservations/", json=reservation_data)
        assert res.status_code == 201, f"La création de réservation a échoué: {res.text}"
        reservation_id = res.json()['reservation_id']
        print(f"  ✅ CREATE Reservation (ID: {reservation_id})")

        # 2. READ Reservation
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/reservations/{reservation_id}")
        assert res.status_code == 200
        print("  ✅ READ Single Reservation")

        # 3. READ OrderItem (vérifier qu'il a bien été créé)
        res = admin_session.get(f"{BASE_URL}{API_PREFIX}/order-item/")
        assert res.status_code == 200
        order_items = [item for item in res.json() if item['reservation_id'] == reservation_id]
        assert len(order_items) == 1
        print("  ✅ READ OrderItem (implicitement créé)")

        # 4. CANCEL Reservation
        res = admin_session.put(f"{BASE_URL}{API_PREFIX}/reservations/{reservation_id}/cancel")
        assert res.status_code == 200
        print("  ✅ CANCEL Reservation")
        
    finally:
        # --- Nettoyage des prérequis ---
        if dish_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/dish/{dish_id}")
            print(f"  🧹 Cleanup: DELETE Dish ({dish_id})")
        if cafeteria_id:
            admin_session.delete(f"{BASE_URL}{API_PREFIX}/cafeteria/{cafeteria_id}")
            print(f"  🧹 Cleanup: DELETE Cafeteria ({cafeteria_id})")