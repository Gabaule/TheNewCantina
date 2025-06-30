import requests

# Base URL for the API
base_url = "http://localhost:8081/api/v1"  # Modifier selon ton URL de base
login_url = "http://localhost:8081/login"

# Utilisateur de test
username = "student1@example.com"  # Remplacer par un email valide d'utilisateur simple
password = "pass123"  # Remplacer par le mot de passe valide

# Liste des endpoints à tester (toutes les routes)
endpoints = [
    ("/cafeteria", "GET"),
    ("/cafeteria/1", "GET"),
    ("/cafeteria", "POST"),
    ("/cafeteria/1", "PUT"),
    ("/cafeteria/1", "DELETE"),
    
    ("/dish", "GET"),
    ("/dish/1", "GET"),
    ("/dish", "POST"),
    ("/dish/1", "PUT"),
    ("/dish/1", "DELETE"),
    
    ("/daily-menu", "GET"),
    ("/daily-menu/1", "GET"),
    ("/daily-menu/by-cafeteria/1", "GET"),
    ("/daily-menu", "POST"),
    ("/daily-menu/1", "PUT"),
    ("/daily-menu/1", "DELETE"),
    
    ("/daily-menu-item/by-menu/1", "GET"),
    ("/daily-menu-item", "POST"),
    ("/daily-menu-item/1", "PUT"),
    ("/daily-menu-item/1", "DELETE"),
    
    ("/reservations", "POST"),
    ("/reservations", "GET"),
    ("/reservations/1", "GET"),
    ("/reservations/1/cancel", "PUT"),
    
    ("/user", "GET"),
    ("/user/1", "GET"),
    ("/user", "POST"),
    ("/user/1", "PUT"),
    ("/user/1", "DELETE"),
    ("/user/balance", "POST"),
]

# Fonction pour se connecter et récupérer le cookie de session
def login():
    # Utiliser une session pour gérer les cookies
    session = requests.Session()

    payload = {"username": username, "password": password}
    response = session.post(login_url, json=payload)
    
    if response.status_code == 200:
        print("[INFO] Login successful")
        return session  # Retourne l'objet session qui contient les cookies
    else:
        print("[ERROR] Login failed:", response.text)
        return None

# Fonction pour tester les routes authentifiées
def test_api(session):
    for endpoint, method in endpoints:
        url = base_url + endpoint
        print(f"Testing {method} {url}...")

        try:
            if method == "GET":
                response = session.get(url)
            elif method == "POST":
                response = session.post(url)
            elif method == "PUT":
                response = session.put(url)
            elif method == "DELETE":
                response = session.delete(url)

            # Vérification de la réponse
            if response.status_code == 200:
                print(f"[PASSED] {method} {url} - OK (200)")
            elif response.status_code == 401:
                print(f"[FAILED] {method} {url} - Unauthorized (401) as expected")
            else:
                print(f"[FAILED] {method} {url} - Status Code: {response.status_code} - Response: {response.text}")
        except Exception as e:
            print(f"[ERROR] {method} {url} - Exception: {str(e)}")

# Exécution du test
if __name__ == "__main__":
    session = login()
    if session:
        test_api(session)
