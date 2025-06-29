# test/test_scenarios.py

import requests
import json
import time

# --- Configuration ---
BASE_URL = "http://localhost:8081" # Assurez-vous que c'est le bon port exposé par Docker

# Identifiants de test (tirés de votre db_seeder.py)
USER_CREDENTIALS = {'username': 'student1@example.com', 'password': 'pass123'}
ADMIN_CREDENTIALS = {'username': 'admin@example.com', 'password': 'password'}

# --- Couleurs pour l'affichage ---
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class TestRunner:
    """Gère l'exécution des tests, les sessions et les statistiques."""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None
        self.passed_count = 0
        self.failed_count = 0

    def start_session(self):
        """Démarre une nouvelle session de test (pour un utilisateur ou invité)."""
        self.session = requests.Session()
        print(f"\n{Colors.BLUE}--- Nouvelle session de test démarrée ---{Colors.RESET}")

    def login(self, credentials, role="utilisateur"):
        """Tente de se connecter et de stocker les cookies de session."""
        print(f"▶️  Tentative de connexion en tant que {role} ({credentials['username']})...")
        try:
            res = self.session.post(f"{self.base_url}/login", data=credentials)
            # Une redirection réussie (302) après un POST de login est un succès.
            if res.status_code == 200 and 'dashboard' in res.url:
                 print(f"{Colors.GREEN}  [PASS] Connexion réussie.{Colors.RESET}")
                 return True
            else:
                print(f"{Colors.RED}  [FAIL] Échec de la connexion. Status: {res.status_code}, URL: {res.url}{Colors.RESET}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}  [FAIL] Erreur de connexion : {e}{Colors.RESET}")
            return False
            
    def logout(self):
        """Se déconnecte pour nettoyer la session."""
        print("▶️  Déconnexion...")
        try:
            self.session.get(f"{self.base_url}/logout")
            print(f"{Colors.GREEN}  [PASS] Déconnexion effectuée.{Colors.RESET}")
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}  [FAIL] Erreur de déconnexion : {e}{Colors.RESET}")

    def run_test(self, description, method, endpoint, expected_status, json_data=None):
        """Exécute un test individuel et affiche le résultat."""
        full_url = self.base_url + endpoint
        print(f"\n▶️  TEST: {description}")
        print(f"   {method.upper()} {full_url}")

        try:
            response = self.session.request(method, full_url, json=json_data, timeout=10)
            
            if response.status_code == expected_status:
                print(f"{Colors.GREEN}  [PASS] Reçu statut {response.status_code} comme attendu.{Colors.RESET}")
                self.passed_count += 1
                return response
            else:
                print(f"{Colors.RED}  [FAIL] Statut attendu {expected_status}, mais reçu {response.status_code}.{Colors.RESET}")
                try:
                    print(f"     {Colors.YELLOW}Réponse: {response.json()}{Colors.RESET}")
                except json.JSONDecodeError:
                    print(f"     {Colors.YELLOW}Réponse: {response.text[:150]}...{Colors.RESET}")
                self.failed_count += 1
                return response

        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}  [FAIL] La requête a échoué: {e}{Colors.RESET}")
            self.failed_count += 1
            return None

    def print_summary(self):
        """Affiche le résumé final des tests."""
        total = self.passed_count + self.failed_count
        print("\n" + "="*50)
        print("                  Résumé des tests")
        print("="*50)
        print(f"  Tests totaux exécutés : {total}")
        print(f"{Colors.GREEN}  Réussis : {self.passed_count}{Colors.RESET}")
        print(f"{Colors.RED}  Échoués : {self.failed_count}{Colors.RESET}")
        print("="*50)


def main():
    runner = TestRunner(BASE_URL)

    # =======================================================
    # == Scénario 1: Utilisateur non authentifié (Invité) ==
    # =======================================================
    print(f"\n{Colors.BLUE}********** DÉBUT DES TESTS EN TANT QU'INVITÉ **********{Colors.RESET}")
    runner.start_session()
    
    runner.run_test(
        description="Un invité peut lister les cafétérias (route publique)",
        method="get", endpoint="/api/v1/cafeteria/",
        expected_status=200
    )
    runner.run_test(
        description="Un invité NE PEUT PAS créer de réservation",
        method="post", endpoint="/api/v1/reservations/",
        expected_status=401 # 401 Unauthorized
    )
    runner.run_test(
        description="Un invité NE PEUT PAS créer de cafétéria",
        method="post", endpoint="/api/v1/cafeteria/",
        json_data={"name": "Test Cafeteria"},
        expected_status=401 # 401 Unauthorized
    )


    # =======================================================
    # == Scénario 2: Utilisateur Standard (student)        ==
    # =======================================================
    print(f"\n{Colors.BLUE}********** DÉBUT DES TESTS EN TANT QU'UTILISATEUR STANDARD **********{Colors.RESET}")
    runner.start_session()
    if runner.login(USER_CREDENTIALS, "Utilisateur Standard"):
        runner.run_test(
            description="Un utilisateur peut lister les cafétérias",
            method="get", endpoint="/api/v1/cafeteria/",
            expected_status=200
        )
        runner.run_test(
            description="Un utilisateur PEUT créditer son propre solde",
            method="post", endpoint="/api/v1/user/balance",
            json_data={"amount": "10.50"},
            expected_status=200
        )
        runner.run_test(
            description="Un utilisateur peut créer une réservation (si le plat existe)",
            method="post", endpoint="/api/v1/reservations/",
            json_data={"cafeteria_id": 1, "items": [{"dish_id": 2, "quantity": 1, "is_takeaway": False}]},
            expected_status=201 # 201 Created
        )
        runner.run_test(
            description="Un utilisateur NE PEUT PAS lister tous les utilisateurs",
            method="get", endpoint="/api/v1/user/",
            expected_status=403 # 403 Forbidden
        )
        runner.run_test(
            description="Un utilisateur NE PEUT PAS supprimer une cafétéria",
            method="delete", endpoint="/api/v1/cafeteria/1",
            expected_status=403 # 403 Forbidden
        )
        runner.logout()

    # =======================================================
    # == Scénario 3: Administrateur                         ==
    # =======================================================
    print(f"\n{Colors.BLUE}********** DÉBUT DES TESTS EN TANT QU'ADMINISTRATEUR **********{Colors.RESET}")
    runner.start_session()
    if runner.login(ADMIN_CREDENTIALS, "Administrateur"):
        runner.run_test(
            description="Un admin PEUT lister tous les utilisateurs",
            method="get", endpoint="/api/v1/user/",
            expected_status=200
        )
        
        # Test de création puis suppression pour être sûr que l'objet existe
        new_cafeteria_data = {
            "name": f"Cafeteria Test {int(time.time())}", # Nom unique pour éviter les conflits
            "address": "123 Rue des Tests",
            "phone": "9876543210"
        }
        res = runner.run_test(
            description="Un admin PEUT créer une nouvelle cafétéria",
            method="post", endpoint="/api/v1/cafeteria/",
            json_data=new_cafeteria_data,
            expected_status=201 # 201 Created
        )
        
        if res and res.status_code == 201:
            cafeteria_id = res.json().get('cafeteria_id')
            runner.run_test(
                description="Un admin PEUT supprimer la cafétéria qu'il vient de créer",
                method="delete", endpoint=f"/api/v1/cafeteria/{cafeteria_id}",
                expected_status=200
            )
        
        runner.logout()
        
    # --- Affichage du résumé ---
    runner.print_summary()
    
    # Quitter avec un code d'erreur si des tests ont échoué (utile pour l'intégration continue)
    if runner.failed_count > 0:
        exit(1)


if __name__ == "__main__":
    main()