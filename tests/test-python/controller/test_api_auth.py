# tests/test-python/controller/test_api_user_flow.py

import pytest
import requests
from datetime import date
from decimal import Decimal

# --- CONFIGURATION ---
BASE_URL = "http://localhost:8081"
API_PREFIX = "/api/v1"

# Identifiants pour un utilisateur standard (défini dans votre db_seeder.py)
USER_CREDENTIALS = {
    "username": "student1@example.com",
    "password": "pass123"
}
# L'ID de cet utilisateur est 1, car c'est le premier créé dans le seeder
USER_ID = 1

@pytest.fixture(scope="session")
def user_session():
    """
    Fixture Pytest pour s'authentifier une seule fois en tant qu'utilisateur standard
    pour toute la session de test.
    """
    print("\n--- (Setup Fixture) Authentification Utilisateur Standard ---")
    s = requests.Session()
    login_url = f"{BASE_URL}/login"
    
    response = s.post(login_url, data=USER_CREDENTIALS, timeout=5)
    
    assert response.status_code == 200, "Le login de l'utilisateur a retourné un code d'erreur"
    assert "session" in s.cookies, "Le cookie de session est manquant après le login."
    # Un utilisateur standard est redirigé vers /dashboard, pas /admin/dashboard
    assert "dashboard" in response.url, "La page après login ne semble pas être le dashboard utilisateur."
    
    print("--- Authentification utilisateur réussie. Début des tests de flux. ---")
    yield s
    print("\n--- Fin de la session de test utilisateur. ---")


def test_user_profile_management(user_session):
    """
    Teste si un utilisateur peut voir et modifier ses propres informations de profil.
    """
    print("\n--- Test: Gestion du profil utilisateur ---")
    
    # --- 1. Lecture des informations initiales ---
    res_get_initial = user_session.get(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}")
    assert res_get_initial.status_code == 200, f"La lecture du profil a échoué: {res_get_initial.text}"
    initial_data = res_get_initial.json()
    initial_first_name = initial_data['first_name']
    print(f"  ✅ READ: Profil initial lu avec succès (Nom: {initial_first_name})")

    try:
        # --- 2. Mise à jour du profil ---
        update_data = {"first_name": "PytestUpdated"}
        res_update = user_session.put(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}", json=update_data)
        assert res_update.status_code == 200, f"La mise à jour du profil a échoué: {res_update.text}"
        assert res_update.json()['first_name'] == "PytestUpdated"
        print("  ✅ UPDATE: Prénom mis à jour avec succès")

    finally:
        # --- 3. Nettoyage : restaurer le nom d'origine ---
        cleanup_data = {"first_name": initial_first_name}
        res_cleanup = user_session.put(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}", json=cleanup_data)
        assert res_cleanup.status_code == 200, "Le nettoyage du profil a échoué"
        print(f"  🧹 CLEANUP: Prénom restauré à '{initial_first_name}'")


def test_user_balance_management(user_session):
    """
    Teste si un utilisateur peut ajouter des fonds à son solde.
    """
    print("\n--- Test: Gestion du solde utilisateur ---")

    # --- 1. Obtenir le solde initial ---
    res_get_initial = user_session.get(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}")
    assert res_get_initial.status_code == 200
    initial_balance = Decimal(str(res_get_initial.json()['balance']))
    print(f"  - Solde initial: {initial_balance:.2f} €")

    # --- 2. Ajouter des fonds ---
    amount_to_add = Decimal("15.50")
    res_add_balance = user_session.post(f"{BASE_URL}{API_PREFIX}/user/balance", json={"amount": str(amount_to_add)})
    assert res_add_balance.status_code == 200, f"L'ajout au solde a échoué: {res_add_balance.text}"
    
    response_data = res_add_balance.json()
    new_balance_from_response = Decimal(str(response_data['new_balance']))
    expected_balance = initial_balance + amount_to_add
    
    assert new_balance_from_response == expected_balance, "Le nouveau solde dans la réponse est incorrect"
    print(f"  ✅ ADD: {amount_to_add:.2f} € ajoutés. Nouveau solde attendu: {expected_balance:.2f} €")

    # --- 3. Vérifier la persistance du nouveau solde ---
    res_get_final = user_session.get(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}")
    assert res_get_final.status_code == 200
    final_balance = Decimal(str(res_get_final.json()['balance']))
    assert final_balance == expected_balance, "Le solde n'a pas été correctement persisté en base de données"
    print(f"  ✅ VERIFY: Le nouveau solde de {final_balance:.2f} € est bien persisté.")


def test_view_menus(user_session):
    """
    Teste si un utilisateur peut consulter les menus disponibles.
    """
    print("\n--- Test: Consultation des menus ---")
    
    # Votre seeder crée des menus pour la semaine du 2025-06-30
    menu_date = "2025-06-30"
    cafeteria_id = 1 # On suppose que la cafétéria 1 existe

    res = user_session.get(f"{BASE_URL}{API_PREFIX}/daily-menu/by-cafeteria/{cafeteria_id}?date={menu_date}")
    assert res.status_code == 200
    
    menu_data = res.json()
    assert "menu" in menu_data
    assert isinstance(menu_data['menu'], list)
    assert len(menu_data['menu']) > 0, f"Aucun menu trouvé pour la cafétéria {cafeteria_id} à la date {menu_date}"
    print(f"  ✅ MENU: Menu pour la cafétéria {cafeteria_id} le {menu_date} récupéré avec succès.")


def test_user_order_flow(user_session):
    """
    Teste le flux complet de commande : trouver un plat, commander, vérifier le solde,
    voir l'historique, puis annuler.
    """
    print("\n--- Test: Flux de commande complet ---")
    reservation_id = None
    try:
        # --- 1. Trouver un plat disponible à commander ---
        menu_date = "2025-07-01" # Un autre jour du seeder
        cafeteria_id = 1
        res_menu = user_session.get(f"{BASE_URL}{API_PREFIX}/daily-menu/by-cafeteria/{cafeteria_id}?date={menu_date}")
        assert res_menu.status_code == 200 and len(res_menu.json()['menu']) > 0
        
        dish_to_order = res_menu.json()['menu'][0]
        dish_id = dish_to_order['dish_id']
        dish_price = Decimal(str(dish_to_order['price']))
        print(f"  ➡️ Prérequis: Plat trouvé (ID: {dish_id}, Prix: {dish_price:.2f} €)")

        # --- 2. Obtenir le solde initial ---
        res_get_initial = user_session.get(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}")
        initial_balance = Decimal(str(res_get_initial.json()['balance']))
        print(f"  - Solde avant commande: {initial_balance:.2f} €")

        # --- 3. Passer la commande (créer une réservation) ---
        order_payload = {
            "cafeteria_id": cafeteria_id,
            "items": [{"dish_id": dish_id, "quantity": 1}]
        }
        res_order = user_session.post(f"{BASE_URL}{API_PREFIX}/reservations/", json=order_payload)
        assert res_order.status_code == 201, f"La création de la réservation a échoué: {res_order.text}"
        reservation_id = res_order.json()['reservation_id']
        print(f"  ✅ CREATE: Commande passée avec succès (Reservation ID: {reservation_id})")

        # --- 4. Vérifier la déduction du solde ---
        res_get_after_order = user_session.get(f"{BASE_URL}{API_PREFIX}/user/{USER_ID}")
        balance_after_order = Decimal(str(res_get_after_order.json()['balance']))
        expected_balance = initial_balance - dish_price
        assert balance_after_order == expected_balance, "Le solde n'a pas été correctement débité"
        print(f"  ✅ VERIFY BALANCE: Solde mis à jour à {balance_after_order:.2f} €")
        
        # --- 5. Vérifier la présence dans l'historique des commandes ---
        res_history = user_session.get(f"{BASE_URL}{API_PREFIX}/reservations/")
        assert res_history.status_code == 200
        assert any(r['reservation_id'] == reservation_id for r in res_history.json()), "La commande n'apparaît pas dans l'historique"
        print("  ✅ VERIFY HISTORY: Commande trouvée dans l'historique personnel.")

    finally:
        # --- 6. Nettoyage : Annuler la réservation pour restaurer le solde ---
        if reservation_id:
            res_cancel = user_session.put(f"{BASE_URL}{API_PREFIX}/reservations/{reservation_id}/cancel")
            assert res_cancel.status_code == 200, f"L'annulation de la réservation a échoué: {res_cancel.text}"
            
            refund_data = res_cancel.json()
            final_balance = Decimal(str(refund_data['new_balance']))
            
            # On vérifie que le solde final est bien revenu à sa valeur initiale
            assert final_balance == initial_balance, "Le remboursement après annulation est incorrect"
            print(f"  🧹 CLEANUP: Commande annulée et solde restauré à {final_balance:.2f} €")