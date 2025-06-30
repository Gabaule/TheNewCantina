import requests

# Base URL for the API
base_url = "http://localhost:8081/api/v1"  # Modifier selon ton URL de base

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

# Fonction pour tester les routes
def test_api():
    for endpoint, method in endpoints:
        url = base_url + endpoint
        print(f"Testing {method} {url}...")

        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url)
        elif method == "PUT":
            response = requests.put(url)
        elif method == "DELETE":
            response = requests.delete(url)

        # Vérification de la réponse
        if response.status_code == 401:
            print(f"[PASSED] {method} {url} - Unauthorized (401) as expected")
        else:
            print(f"[FAILED] {method} {url} - Status Code: {response.status_code} - Response: {response.text}")

# Exécution du test
if __name__ == "__main__":
    test_api()
