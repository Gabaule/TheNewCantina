import pytest
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8081"
LOGIN_URL = f"{BASE_URL}/login"
API_URL = f"{BASE_URL}/api/v1"

ADMIN_CREDENTIALS = {
    "username": "admin@example.com",
    "password": "password"
}

# Définir ici tous les endpoints à tester
ENDPOINTS = [
    # method, url, description, (optionnel: json data)
    ("GET",    f"{API_URL}/user/",        "Liste users",            None),
    ("POST",   f"{API_URL}/user/",        "Créer user",             {
        "last_name": "Pytest", "first_name": "Admin", "email": "admin_pytest@example.com", "password": "testpw", "role": "student", "balance": 5}),
    ("GET",    f"{API_URL}/cafeteria/",   "Liste cafet",            None),
    ("POST",   f"{API_URL}/cafeteria/",   "Créer cafet",            {"name": "CafetPytest"}),
    ("GET",    f"{API_URL}/dish/",        "Liste plats",            None),
    ("POST",   f"{API_URL}/dish/",        "Créer plat",             {
        "name": "PlatPytest", "description": "desc", "dine_in_price": 2.5, "dish_type": "main_course"}),
    # Ajoute d'autres endpoints ici selon ton besoin
]

@pytest.fixture(scope="session")
def admin_session():
    """Crée une session requests loggée en admin, gère le CSRF si besoin."""
    s = requests.Session()
    r = s.get(LOGIN_URL)
    csrf_token = None
    if 'csrf_token' in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find('input', {'name': 'csrf_token'})
        if csrf:
            csrf_token = csrf['value']
    data = {
        "username": ADMIN_CREDENTIALS["username"],
        "password": ADMIN_CREDENTIALS["password"],
    }
    if csrf_token:
        data["csrf_token"] = csrf_token
    resp = s.post(LOGIN_URL, data=data, allow_redirects=True)
    assert "Identifiants incorrects" not in resp.text, "Erreur de login admin (mauvais identifiants)"
    assert "session" in s.cookies, "Login admin échoué : pas de cookie session !"
    return s

@pytest.mark.parametrize("method,url,desc,json_data", [
    pytest.param(*ep, id=ep[2]) for ep in ENDPOINTS
])
def test_admin_endpoints(admin_session, method, url, desc, json_data):
    """Teste chaque endpoint admin."""
    response = admin_session.request(method, url, json=json_data, allow_redirects=True)
    # Critères de succès par défaut : 200, 201, 204
    assert response.status_code in (200, 201, 204), \
        f"{desc} [{method} {url}] a échoué - code {response.status_code} - body: {response.text[:200]}"

def test_bilan_admin_endpoints(admin_session, capsys):
    """(Optionnel) Affiche un mini-bilan à la fin des tests admin (bonus, pas indispensable avec pytest)"""
    print("\nPytest va générer un bilan automatique. Les tests OK/K0 s'affichent ci-dessus. 👆")
    print("Si tu veux un rapport HTML : pytest --html=rapport.html")

