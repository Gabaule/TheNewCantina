# tests/test-python/controller/test_api_admin_auth.py

import pytest
from datetime import date, timedelta
from app.models import db, AppUser, Cafeteria, Dish, DailyMenu

# Le préfixe de l'API est maintenant défini ici pour être réutilisé
API_PREFIX = "/api/v1"

@pytest.fixture
def admin_client(client):
    """
    Fixture Pytest qui retourne un client de test authentifié en tant qu'admin.
    'client' provient de la fixture globale dans conftest.py.
    """
    # Données de connexion pour l'admin créé par le seeder
    credentials = {
        "username": "admin@example.com",
        "password": "password"
    }
    # Utilisation du client de test pour simuler le POST sur /login
    response = client.post('/login', data=credentials, follow_redirects=True)
    
    # Vérifie que la connexion a bien eu lieu (statut 200 après redirection)
    assert response.status_code == 200, "La connexion de l'admin a échoué."
    # Vérifie que le dashboard admin est bien affiché
    assert b"Admin Dashboard" in response.data or b"Manage Daily Menus" in response.data
    
    # Le client garde maintenant le cookie de session pour les requêtes suivantes
    yield client
    
    # Déconnexion propre à la fin du test
    client.get('/logout')

def test_user_crud(admin_client):
    """Teste les opérations CRUD complètes sur l'endpoint des utilisateurs."""
    print("\n--- Test des Endpoints: Utilisateurs (User) ---")
    user_data = {
        "last_name": "TestPytest",
        "first_name": "Utilisateur",
        "email": f"test.user.pytest.{date.today().isoformat()}@example.com",
        "password": "password123",
        "role": "student",
        "balance": 20.0
    }
    user_id = None
    try:
        # 1. CREATE
        res = admin_client.post(f"{API_PREFIX}/user/", json=user_data)
        assert res.status_code == 201, f"CREATE User a échoué: {res.get_data(as_text=True)}"
        created_user = res.get_json()
        user_id = created_user['user_id']
        print(f"  ✅ CREATE User (ID: {user_id})")

        # 2. READ (List)
        res = admin_client.get(f"{API_PREFIX}/user/")
        assert res.status_code == 200
        assert any(u['user_id'] == user_id for u in res.get_json()), "Utilisateur créé non trouvé dans la liste"
        print("  ✅ READ User List")

        # 3. READ (Single)
        res = admin_client.get(f"{API_PREFIX}/user/{user_id}")
        assert res.status_code == 200
        assert res.get_json()['email'] == user_data['email']
        print("  ✅ READ Single User")

        # 4. UPDATE
        update_data = {"last_name": "TestModifie", "role": "staff"}
        res = admin_client.put(f"{API_PREFIX}/user/{user_id}", json=update_data)
        assert res.status_code == 200
        assert res.get_json()['last_name'] == "TestModifie"
        print("  ✅ UPDATE User")

    finally:
        # 5. DELETE (Cleanup)
        if user_id:
            res = admin_client.delete(f"{API_PREFIX}/user/{user_id}")
            assert res.status_code == 200, "Le nettoyage de l'utilisateur a échoué"
            print("  ✅ DELETE User (Cleanup)")

def test_cafeteria_crud(admin_client):
    """Teste les opérations CRUD complètes sur l'endpoint des cafétérias."""
    print("\n--- Test des Endpoints: Cafétérias (Cafeteria) ---")
    cafeteria_data = {"name": "Cafeteria de Test Pytest"}
    cafeteria_id = None
    try:
        # 1. CREATE
        res = admin_client.post(f"{API_PREFIX}/cafeteria/", json=cafeteria_data)
        assert res.status_code == 201
        cafeteria_id = res.get_json()['cafeteria_id']
        print(f"  ✅ CREATE Cafeteria (ID: {cafeteria_id})")

        # 2. READ (List & Single)
        res = admin_client.get(f"{API_PREFIX}/cafeteria/")
        assert res.status_code == 200
        assert any(c['cafeteria_id'] == cafeteria_id for c in res.get_json())
        print("  ✅ READ Cafeteria List")

        res = admin_client.get(f"{API_PREFIX}/cafeteria/{cafeteria_id}")
        assert res.status_code == 200
        print("  ✅ READ Single Cafeteria")

        # 3. UPDATE
        res = admin_client.put(f"{API_PREFIX}/cafeteria/{cafeteria_id}", json={"name": "Nouveau Nom Cafe Pytest"})
        assert res.status_code == 200
        assert res.get_json()['name'] == "Nouveau Nom Cafe Pytest"
        print("  ✅ UPDATE Cafeteria")

    finally:
        # 4. DELETE (Cleanup)
        if cafeteria_id:
            res = admin_client.delete(f"{API_PREFIX}/cafeteria/{cafeteria_id}")
            assert res.status_code == 200
            print("  ✅ DELETE Cafeteria (Cleanup)")

def test_dish_crud(admin_client):
    """Teste les opérations CRUD complètes sur l'endpoint des plats."""
    print("\n--- Test des Endpoints: Plats (Dish) ---")
    dish_data = {"name": "Plat de Test Pytest", "description": "Un plat pour pytest.", "dine_in_price": 9.99, "dish_type": "main_course"}
    dish_id = None
    try:
        # 1. CREATE
        res = admin_client.post(f"{API_PREFIX}/dish/", json=dish_data)
        assert res.status_code == 201, f"CREATE Dish a échoué: {res.get_data(as_text=True)}"
        dish_id = res.get_json()['dish_id']
        print(f"  ✅ CREATE Dish (ID: {dish_id})")

        # 2. READ (List)
        res = admin_client.get(f"{API_PREFIX}/dish/")
        assert res.status_code == 200
        assert any(d['dish_id'] == dish_id for d in res.get_json()), "Le plat créé est introuvable."
        print("  ✅ READ Dish List")
        
        # 3. UPDATE
        res = admin_client.put(f"{API_PREFIX}/dish/{dish_id}", json={"dine_in_price": 12.50})
        assert res.status_code == 200 and res.get_json()['dine_in_price'] == 12.50
        print("  ✅ UPDATE Dish")
        
    finally:
        # 4. DELETE (Cleanup)
        if dish_id:
            res = admin_client.delete(f"{API_PREFIX}/dish/{dish_id}")
            assert res.status_code == 200, f"Le nettoyage du plat a échoué: {res.get_data(as_text=True)}"
            print("  ✅ DELETE Dish (Cleanup)")

def test_menu_and_item_crud(admin_client):
    """Teste les endpoints pour les menus et leurs items, en gérant les dépendances."""
    print("\n--- Test des Endpoints: Menus (DailyMenu & DailyMenuItem) ---")
    
    # --- Création des prérequis directement en base de données ---
    # C'est plus rapide et plus fiable que de passer par l'API pour les prérequis
    caf = Cafeteria(name="Café pour Menu Pytest")
    dish = Dish(name="Plat pour Menu Pytest", dine_in_price=5, dish_type="soup")
    db.session.add_all([caf, dish])
    db.session.commit()
    print(f"  ➡️ Prérequis: Création cafétéria (ID: {caf.cafeteria_id}) et plat (ID: {dish.dish_id})")
    
    # --- Tests DailyMenu ---
    menu_date_str = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')
    res_menu = admin_client.post(f"{API_PREFIX}/daily-menu/", json={"cafeteria_id": caf.cafeteria_id, "menu_date": menu_date_str})
    assert res_menu.status_code == 201
    menu_id = res_menu.get_json()['menu_id']
    print(f"  ✅ CREATE DailyMenu (ID: {menu_id})")

    # --- Tests DailyMenuItem ---
    item_data = {"menu_id": menu_id, "dish_id": dish.dish_id, "dish_role": "soup", "display_order": 1}
    res_item = admin_client.post(f"{API_PREFIX}/daily-menu-item/", json=item_data)
    assert res_item.status_code == 201
    item_id = res_item.get_json()['menu_item_id']
    print(f"  ✅ CREATE DailyMenuItem (ID: {item_id})")

    # --- Vérification et Nettoyage ---
    res_check = admin_client.get(f"{API_PREFIX}/daily-menu-item/by-menu/{menu_id}")
    assert res_check.status_code == 200 and any(i['menu_item_id'] == item_id for i in res_check.get_json())
    print("  ✅ READ MenuItem List")
    
    # La suppression du menu devrait supprimer les items en cascade (défini dans le modèle)
    res_del_menu = admin_client.delete(f"{API_PREFIX}/daily-menu/{menu_id}")
    assert res_del_menu.status_code == 200
    print(f"  🧹 Cleanup: DELETE DailyMenu ({menu_id}), ce qui devrait supprimer l'item en cascade.")