# Test Execution Report

## 📊 Summary
| Metric          | Value |
|-----------------|-------|
| **Total Tests** | 161 |
| ✅ Passed       | 155 |
| ❌ Failed/Error   | 6 |
| ⏭️ Skipped       | 0 |

---

## 📄 Detailed Test Case Results

### API_001: Verify full CRUD (Create, Read, Update, Delete) for the User API endpoint.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.4360s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_crud` |


**Prerequisites:**
1. An authenticated admin client.

**Test Scenario:**
An admin must be able to manage users through the API.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Send POST to `/api/v1/user/` to create a new user. | Receives HTTP 201 and user data. | As Expected | **Pass** |
| 2 | Send GET to `/api/v1/user/` to list all users. | Receives HTTP 200 and the new user is in the list. | As Expected | **Pass** |
| 3 | Send PUT to `/api/v1/user/{id}` to update the user. | Receives HTTP 200 and updated data. | As Expected | **Pass** |
| 4 | Send DELETE to `/api/v1/user/{id}` to delete the user. | Receives HTTP 200. | As Expected | **Pass** |

---

### API_002: Verify full CRUD for the Cafeteria API endpoint.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_002` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3590s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_cafeteria_crud` |


**Prerequisites:**
1. An authenticated admin client.

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Perform Create, Read, Update, Delete operations on the Cafeteria API. | All operations succeed with correct HTTP status codes. | As Expected | **Pass** |

---

### API_003: Verify full CRUD for the Dish API endpoint.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_003` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3520s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_dish_crud` |


**Prerequisites:**
1. An authenticated admin client.

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Perform Create, Read, Update, Delete operations on the Dish API. | All operations succeed with correct HTTP status codes. | As Expected | **Pass** |

---

### API_004: Verify creation of Menus and linking Menu Items via API.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_004` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3500s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_menu_and_item_crud` |


**Prerequisites:**
1. Authenticated admin client.
1. A Cafeteria and a Dish exist.

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Create a DailyMenu via POST request. | Receives HTTP 201. | As Expected | **Pass** |
| 2 | Create a DailyMenuItem linking the menu and a dish. | Receives HTTP 201. | As Expected | **Pass** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3610s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config0]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3520s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config1]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3550s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config2]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3540s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config3]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3550s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config4]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3680s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config5]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3610s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config6]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3510s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config7]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3800s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config8]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3510s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config9]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3560s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config10]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3520s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config11]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3490s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_user_api_permissions[endpoint_config12]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

---

### E2E_001: Verify Admin Login and Logout functionality through the UI.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.4250s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_loginAdminLogOut` |


**Prerequisites:**
1. Application is running.
1. Default admin user exists.

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Navigate to login page. | Page loads. | As Expected | **Pass** |
| 2 | Enter admin credentials and submit. | Redirected to admin dashboard. | As Expected | **Pass** |
| 3 | Click the 'Logout' link. | Redirected to login page. | As Expected | **Pass** |

---

### SCEN_001: Test the full lifecycle of user management from creation to deletion at the model level.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `SCEN_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.6890s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Passed** |
| **Test Function**| `test_complete_user_lifecycle` |


**Prerequisites:**
None

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Execute create, update, and delete functions on the AppUser model. | All model methods execute without error and reflect correct state changes in the database. | As Expected | **Pass** |

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3490s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_user_api_permissions[endpoint_config13]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

**Failure Details:**
```
authenticated_client = <FlaskClient <Flask 'app.controller.controller'>>
endpoint_config = {'allowed': False, 'desc': "Voir la réservation d'un autre", 'method': 'GET', 'url': '/api/v1/reservations/{other_user_reservation_id}'}

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
>           assert response.status_code in {401, 403}, f"Accès AUTORISÉ à un endpoint qui devait être refusé.\n{debug_info}"
E           AssertionError: Accès AUTORISÉ à un endpoint qui devait être refusé.
E             Endpoint: GET /api/v1/reservations/1
E             Description: Voir la réservation d'un autre
E             Attendu: Refusé (401/403)
E             Reçu: 404
E             Réponse: {"error":"Reservation not found."}
E             
E           assert 404 in {401, 403}
E            +  where 404 = <WrapperTestResponse 35 bytes [404 NOT FOUND]>.status_code

tests/test-python/controller/test_api_auth.py:93: AssertionError
```

---

### API_SEC_001: Verify API permissions for a standard authenticated user.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `API_SEC_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3470s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_user_api_permissions[endpoint_config14]` |


**Prerequisites:**
None

**Test Scenario:**
A standard user should be able to access their own data but be denied access to other users' data or admin-only endpoints.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Attempt to access admin-only endpoints (e.g., list all users). | Access is denied with HTTP 401/403. | As Expected | **Pass** |
| 2 | Attempt to access own user data. | Access is allowed with HTTP 200. | As Expected | **Pass** |
| 3 | Attempt to access another user's data (e.g., another user's reservation). | Access is denied with HTTP 401/403/404. | Execution failed. See details below. | **Failed** |

**Failure Details:**
```
authenticated_client = <FlaskClient <Flask 'app.controller.controller'>>
endpoint_config = {'allowed': False, 'desc': "Annuler la réservation d'un autre", 'method': 'PUT', 'url': '/api/v1/reservations/{other_user_reservation_id}/cancel'}

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
>           assert response.status_code in {401, 403}, f"Accès AUTORISÉ à un endpoint qui devait être refusé.\n{debug_info}"
E           AssertionError: Accès AUTORISÉ à un endpoint qui devait être refusé.
E             Endpoint: PUT /api/v1/reservations/1/cancel
E             Description: Annuler la réservation d'un autre
E             Attendu: Refusé (401/403)
E             Reçu: 404
E             Réponse: {"error":"Reservation not found."}
E             
E           assert 404 in {401, 403}
E            +  where 404 = <WrapperTestResponse 35 bytes [404 NOT FOUND]>.status_code

tests/test-python/controller/test_api_auth.py:93: AssertionError
```

---

### E2E_002: Verify a student can log in and attempt to order a meal.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `E2E_002` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `3.2460s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_orderfoodinthepast` |


**Prerequisites:**
1. Application is running.
1. Default student user exists.

**Test Scenario:**
N/A

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Navigate to login page and log in as a student. | Redirected to user dashboard. | As Expected | **Pass** |
| 2 | Select a cafeteria from the navigation. | The menu for that cafeteria is displayed. | As Expected | **Pass** |
| 3 | Add an item to the cart. | The item appears in the cart summary. | As Expected | **Pass** |
| 4 | Click 'Place Order'. | The order is confirmed and user is redirected to order history. | Execution failed. See details below. | **Failed** |

**Failure Details:**
```
self = <test_orderfoodinthepast.TestOrderfoodinthepast object at 0x10657ad50>

    def test_orderfoodinthepast(self):
      self.driver.get("http://localhost:8081/login")
      self.driver.set_window_size(1512, 888)
      self.driver.find_element(By.ID, "username").click()
      self.driver.find_element(By.ID, "username").send_keys("student1@example.com")
      self.driver.find_element(By.ID, "password").send_keys("pass123")
      self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
>     self.driver.find_element(By.LINK_TEXT, "Kafeteria").click()
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test-python/selenium-e2e/test_orderfoodinthepast.py:28: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/webdriver.py:922: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/webdriver.py:454: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x10e06c550>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"Unable to locate element: Kafeteria","stacktr.../content/shared/webdriver/Errors.sys.mjs:552:5\\ndom.find/</<@chrome://remote/content/shared/DOM.sys.mjs:136:16\\n"}}'}

    def check_response(self, response: dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                try:
                    value = json.loads(value_json)
                    if isinstance(value, dict):
                        if len(value) == 1:
                            value = value["value"]
                        status = value.get("error", None)
                        if not status:
                            status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                            message = value.get("value") or value.get("message")
                            if not isinstance(message, str):
                                value = message
                                message = message.get("message")
                        else:
                            message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: Kafeteria; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#nosuchelementexception
E       Stacktrace:
E       RemoteError@chrome://remote/content/shared/RemoteError.sys.mjs:8:8
E       WebDriverError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:199:5
E       NoSuchElementError@chrome://remote/content/shared/webdriver/Errors.sys.mjs:552:5
E       dom.find/</<@chrome://remote/content/shared/DOM.sys.mjs:136:16

../../../.pyenv/versions/3.13.3/envs/devenvone/lib/python3.13/site-packages/selenium/webdriver/remote/errorhandler.py:232: NoSuchElementException
```

---

### MODEL_DB_001: Verify database uniqueness constraint for (cafeteria_id, menu_date) on update.
| Attribute | Value |
| :--- | :--- |
| **Test Case ID** | `MODEL_DB_001` |
| **Version** | `1.0` |
| **Tester** | `Automation` |
| **Execution Time** | `0.3050s` |
| **Date Tested** | `08-Jul-2025` |
| **Final Status** | **Failed** |
| **Test Function**| `test_menu_uniqueness_constraint_on_update` |


**Prerequisites:**
None

**Test Scenario:**
The system should prevent a menu from being updated to a date/cafeteria combination that already exists for another menu.

**Test Steps:**
| Step # | Step Details | Expected Results | Actual Results | Status |
|:---:|:---|:---|:---|:---:|
| 1 | Create Menu A for Cafeteria 1 on Date X. | Menu is created. | As Expected | **Pass** |
| 2 | Create Menu B for Cafeteria 2 on Date Y. | Menu is created. | As Expected | **Pass** |
| 3 | Attempt to update Menu B to Cafeteria 1 and Date X. | The update operation must fail and return False due to the unique constraint violation. | Execution failed. See details below. | **Failed** |

**Failure Details:**
```
app = <Flask 'app.controller.controller'>

    def test_menu_uniqueness_constraint_on_update(app):
        """Vérifie la contrainte d'unicité (cafeteria_id, menu_date) lors d'une mise à jour."""
        with app.app_context():
            caf1 = Cafeteria.create_cafeteria("Caf 1")
            caf2 = Cafeteria.create_cafeteria("Caf 2")
            db.session.commit()
    
            # Menu existant pour caf1 à une date donnée
            DailyMenu.create_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
    
            # Autre menu pour caf2 qu'on va essayer de déplacer
            menu_to_update = DailyMenu.create_menu(cafeteria_id=caf2.cafeteria_id, menu_date=date(2030, 1, 2))
            db.session.commit()
    
            # Tenter de déplacer le menu vers une date/cafeteria déjà prise
            ok = menu_to_update.update_menu(cafeteria_id=caf1.cafeteria_id, menu_date=date(2030, 1, 1))
>           assert ok is False # La méthode doit retourner False en cas d'échec d'intégrité
            ^^^^^^^^^^^^^^^^^^
E           assert True is False

tests/test-python/models/test_daily_menu.py:61: AssertionError
```

---
