# tests/test-python/selenium-e2e/test_combined_scenarios.py

"""
Combined Test Scenarios
=======================
This module combines existing unit tests into logical business scenarios.
Each scenario represents a complete workflow by calling existing test functions in sequence.
"""
import sys
import os
import pytest
from datetime import date, timedelta

# Fix for ImportError:
# Add the 'tests/test-python' directory to the Python path at runtime.
# This allows us to use absolute imports from the 'models' and 'controller' subdirectories,
# bypassing the issues with relative imports and invalid package names.
# __file__ is the path to this script. We navigate two levels up to get to 'test-python'.
tests_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

# Import existing model tests using absolute paths relative to 'test-python'
from models.test_app_user import (
    test_create_user, test_update_user, test_delete_user, 
    test_unique_email_constraint, test_app_user_get_all_dicts
)
from models.test_cafeteria import (
    test_create_cafeteria, test_update_cafeteria, test_delete_cafeteria,
    test_get_all_dicts as test_cafeteria_get_all_dicts
)
from models.test_dish import (
    test_create_dish, test_update_from_dict, test_delete_dish,
    test_get_all_dishes_as_dicts, test_dish_delete_fails_if_in_use_by_menu_item
)
from models.test_daily_menu import (
    test_create_menu, test_update_menu, test_delete_menu
)
from models.test_daily_menu_item import (
    test_create_menu_item, test_update_menu_item, test_delete_menu_item
)
from models.test_reservation import (
    test_create_reservation, test_update_reservation, test_delete_reservation
)
from models.test_order_item import (
    test_create_order_item, test_update_order_item, test_delete_order_item
)

# Import controller/API tests
from controller.test_api_no_auth import test_api_unauthenticated_access_is_denied

# Import models directly for the rewritten test
from app.models import db, Cafeteria, Dish, DailyMenu, DailyMenuItem


class TestUserManagementScenario:
    """
    Complete User Management Workflow
    Tests the full lifecycle of user management from creation to deletion.
    """
    
    def test_complete_user_lifecycle(self, app):
        """
        SCENARIO: Complete user management workflow
        
        Steps:
        1. Create a new user
        2. Update user information
        3. Test data validation (unique email constraint)
        4. Retrieve all users
        5. Delete the user
        """
        print("\n=== USER MANAGEMENT SCENARIO ===")
        
        print("Step 1: Creating user...")
        test_create_user(app)
        
        print("Step 2: Updating user...")
        test_update_user(app)
        
        print("Step 3: Testing email uniqueness...")
        test_unique_email_constraint(app)
        
        print("Step 4: Retrieving all users...")
        test_app_user_get_all_dicts(app)
        
        print("Step 5: Deleting user...")
        test_delete_user(app)
        
        print("✅ User Management Scenario: COMPLETED")


class TestCafeteriaManagementScenario:
    """
    Complete Cafeteria Management Workflow
    Tests the full lifecycle of cafeteria management.
    """
    
    def test_complete_cafeteria_lifecycle(self, app):
        """
        SCENARIO: Complete cafeteria management workflow
        
        Steps:
        1. Create a new cafeteria
        2. Update cafeteria information
        3. Retrieve all cafeterias
        4. Delete the cafeteria
        """
        print("\n=== CAFETERIA MANAGEMENT SCENARIO ===")
        
        print("Step 1: Creating cafeteria...")
        test_create_cafeteria(app)
        
        print("Step 2: Updating cafeteria...")
        test_update_cafeteria(app)
        
        print("Step 3: Retrieving all cafeterias...")
        test_cafeteria_get_all_dicts(app)
        
        print("Step 4: Deleting cafeteria...")
        test_delete_cafeteria(app)
        
        print("✅ Cafeteria Management Scenario: COMPLETED")


class TestMenuManagementScenario:
    """
    Complete Menu Management Workflow
    Tests the creation and management of daily menus with dishes.
    """
    
    def test_complete_menu_creation_workflow(self, app):
        """
        SCENARIO: Complete menu management workflow (Rewritten for state control)
        
        Steps:
        1. Create a cafeteria and a dish.
        2. Create a daily menu and add the dish to it.
        3. Verify that the in-use dish cannot be deleted (constraint test).
        4. Clean up in the correct order: menu item -> menu -> dish -> cafeteria.
        """
        print("\n=== MENU MANAGEMENT SCENARIO (REWRITTEN) ===")
        
        with app.app_context():
            # Step 1: Create a cafeteria and a dish
            print("Step 1: Creating cafeteria and dish...")
            cafeteria = Cafeteria.create_cafeteria("Integrated Test Cafeteria")
            in_use_dish = Dish.create_dish("Pizza Slice", "A slice of pizza", 2.50, "main_course")
            db.session.commit()
            
            # Step 2: Create a daily menu and add the dish to it
            print("Step 2: Creating menu and linking dish...")
            menu = DailyMenu.create_menu(cafeteria_id=cafeteria.cafeteria_id, menu_date=date.today())
            db.session.commit()
            menu_item = DailyMenuItem.create_menu_item(menu_id=menu.menu_id, dish_id=in_use_dish.dish_id, dish_role="main_course")
            db.session.commit()

            # Step 3: Verify the in-use dish cannot be deleted
            print("Step 3: Verifying constraint (cannot delete in-use dish)...")
            delete_success = in_use_dish.delete_dish()
            assert not delete_success, "An in-use dish should not be deletable."
            assert Dish.get_by_id(in_use_dish.dish_id) is not None, "Dish was deleted when it shouldn't have been."

            # Step 4: Clean up in the correct order
            print("Step 4: Cleaning up in correct order...")
            
            # 4a: Delete the menu item first
            print("  - Deleting menu item...")
            assert menu_item.delete_menu_item(), "Failed to delete the menu item."
            
            # 4b: Now, deleting the dish should work
            print("  - Deleting the now-unused dish...")
            assert in_use_dish.delete_dish(), "Failed to delete the dish after its menu item was removed."
            
            # 4c: Delete the menu
            print("  - Deleting the menu...")
            assert menu.delete_menu(), "Failed to delete the menu."
            
            # 4d: Delete the cafeteria
            print("  - Deleting the cafeteria...")
            assert cafeteria.delete_cafeteria(), "Failed to delete the cafeteria."

            print("✅ Menu Management Scenario: COMPLETED")


class TestOrderWorkflowScenario:
    """
    Complete Order Processing Workflow
    Tests the full order process from creation to completion.
    """
    
    def test_complete_order_workflow(self, app):
        """
        SCENARIO: Complete order processing workflow
        
        Steps:
        1. Set up users and cafeterias
        2. Create dishes and menus
        3. Process reservations
        4. Manage order items
        5. Update and cancel orders
        6. Clean up
        """
        print("\n=== ORDER WORKFLOW SCENARIO ===")
        
        print("Step 1: Setting up users...")
        test_create_user(app)
        
        print("Step 2: Setting up cafeterias...")
        test_create_cafeteria(app)
        
        print("Step 3: Setting up dishes and menus...")
        test_create_dish(app)
        test_create_menu(app)
        test_create_menu_item(app)
        
        print("Step 4: Processing reservations...")
        test_create_reservation(app)
        test_update_reservation(app)
        
        print("Step 5: Managing order items...")
        test_create_order_item(app)
        test_update_order_item(app)
        
        print("Step 6: Cleaning up orders...")
        test_delete_order_item(app)
        test_delete_reservation(app)
        
        print("✅ Order Workflow Scenario: COMPLETED")


class TestSecurityAndAuthScenario:
    """
    Security and Authentication Workflow
    Tests access controls and authentication requirements.
    """
    
    @pytest.mark.parametrize("endpoint_subset", [
        # Test a subset of endpoints to avoid overwhelming the test
        [
            {"method": "GET", "url": "/api/v1/user/", "desc": "Liste tous les utilisateurs"},
            {"method": "POST", "url": "/api/v1/user/", "json": {"first_name": "x", "last_name": "x", "email": "a@b.c", "password": "1"}, "desc": "Créer un utilisateur"},
            {"method": "GET", "url": "/api/v1/cafeteria/", "desc": "Lister les cafétérias"},
            {"method": "POST", "url": "/api/v1/dish/", "json": {"name": "TestPlat", "description": "x", "dine_in_price": 1, "dish_type": "main_course"}, "desc": "Créer un plat"},
        ]
    ])
    def test_unauthenticated_access_security(self, client, endpoint_subset):
        """
        SCENARIO: Security verification workflow
        
        Steps:
        1. Test that unauthenticated users are properly rejected
        2. Verify all protected endpoints require authentication
        """
        print("\n=== SECURITY VERIFICATION SCENARIO ===")
        
        for endpoint in endpoint_subset:
            print(f"Testing security for: {endpoint['method']} {endpoint['url']}")
            test_api_unauthenticated_access_is_denied(client, endpoint)
        
        print("✅ Security Verification Scenario: COMPLETED")


class TestDataIntegrityScenario:
    """
    Data Integrity and Constraints Workflow
    Tests that the system properly enforces data integrity rules.
    """
    
    def test_referential_integrity_workflow(self, app):
        """
        SCENARIO: Data integrity and constraints verification
        
        Steps:
        1. Test unique constraints (email uniqueness)
        2. Test foreign key relationships
        3. Test cascade deletions work properly
        4. Test business rule constraints
        """
        print("\n=== DATA INTEGRITY SCENARIO ===")
        
        print("Step 1: Testing unique constraints...")
        test_unique_email_constraint(app)
        
        print("Step 2: Testing foreign key relationships...")
        # Create related data to test relationships
        test_create_user(app)
        test_create_cafeteria(app)
        test_create_dish(app)
        test_create_menu(app)
        test_create_menu_item(app)
        
        print("Step 3: Testing constraint enforcement...")
        test_dish_delete_fails_if_in_use_by_menu_item(app)
        
        print("Step 4: Testing proper cleanup order...")
        test_delete_menu_item(app)
        test_delete_menu(app)
        test_delete_dish(app)
        test_delete_cafeteria(app)
        test_delete_user(app)
        
        print("✅ Data Integrity Scenario: COMPLETED")


class TestSystemIntegrationScenario:
    """
    Full System Integration Test
    Tests that all components work together in a realistic business scenario.
    """
    
    def test_full_system_integration(self, app, client):
        """
        SCENARIO: Complete system integration test
        
        This scenario simulates a realistic use case:
        1. Admin sets up the system (users, cafeterias, dishes)
        2. Admin creates daily menus
        3. Users place orders
        4. System processes and manages the orders
        5. Cleanup and data integrity verification
        """
        print("\n=== FULL SYSTEM INTEGRATION SCENARIO ===")
        
        print("Phase 1: System Setup...")
        # Admin creates base data
        test_create_user(app)  # Create admin user
        test_create_cafeteria(app)  # Create cafeterias
        test_create_dish(app)  # Create dishes
        
        print("Phase 2: Menu Management...")
        # Admin creates menus
        test_create_menu(app)
        test_create_menu_item(app)
        
        print("Phase 3: Order Processing...")
        # Users interact with the system
        test_create_reservation(app)
        test_create_order_item(app)
        
        print("Phase 4: Order Management...")
        # System manages orders
        test_update_reservation(app)
        test_update_order_item(app)
        
        print("Phase 5: Data Management...")
        # Admin manages data
        test_update_user(app)
        test_update_cafeteria(app)
        test_update_from_dict(app)  # Update dish
        
        print("Phase 6: Security Verification...")
        # Quick security check with a sample endpoint
        sample_endpoint = {"method": "GET", "url": "/api/v1/user/", "desc": "Liste tous les utilisateurs"}
        test_api_unauthenticated_access_is_denied(client, sample_endpoint)
        
        print("Phase 7: System Cleanup...")
        # Proper cleanup order (reverse of creation)
        test_delete_order_item(app)
        test_delete_reservation(app)
        test_delete_menu_item(app)
        test_delete_menu(app)
        test_delete_dish(app)
        test_delete_cafeteria(app)
        test_delete_user(app)
        
        print("✅ Full System Integration Scenario: COMPLETED")


# Utility functions for scenario reporting
def print_scenario_summary():
    """Print a summary of all available scenarios"""
    scenarios = [
        "UserManagementScenario - Complete user lifecycle",
        "CafeteriaManagementScenario - Complete cafeteria lifecycle", 
        "MenuManagementScenario - Menu and dish management",
        "OrderWorkflowScenario - Order processing workflow",
        "SecurityAndAuthScenario - Security verification",
        "DataIntegrityScenario - Data integrity verification",
        "SystemIntegrationScenario - Full system integration"
    ]
    
    print("\n" + "="*60)
    print("AVAILABLE TEST SCENARIOS:")
    print("="*60)
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")
    print("="*60)


if __name__ == "__main__":
    print_scenario_summary()