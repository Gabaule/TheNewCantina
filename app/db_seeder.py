import os
import sys
from datetime import date, datetime

# Add parent directory to path to allow model imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import (
    db, AppUser, Cafeteria, Dish, DailyMenu, DailyMenuItem, Reservation, OrderItem
)

def populate_database_if_empty():
    """Checks if the database is empty and populates it with initial data if it is."""
    # This function should be called from within a Flask app context
    if AppUser.query.first() is not None:
        print("✅ Database already contains data. Skipping population.")
        return

    print("⏳ Database is empty. Populating with initial data...")
    
    try:
        # --- Stage 1: Create independent data (Users, Cafeterias, Dishes) ---
        
        # Create Cafeterias
        cafeterias_names = [
            'AR', 'Fakulta bezpečnostného inžinierstva', 'Fakulta riadenia a inf.',
            'FCC Nová Menza', 'Kafeteria', 'Letisko Hričov', 'Nová Menza', 'Stará Menza'
        ]
        cafeterias = [Cafeteria.create_cafeteria(name=name) for name in cafeterias_names]
        nova_menza = next((c for c in cafeterias if c.name == 'Nová Menza'), cafeterias[0])
            
            # Create Dishes
        dishes_data = [
            # Soups
            {"name": "Vegetable Soup with Vermicelli", "description": "Allergens: gluten, egg, celery", "dine_in_price": 0.00, "dish_type": "soup"},
            {"name": "Lentil Soup", "description": "Allergens: celery", "dine_in_price": 0.00, "dish_type": "soup"},
            {"name": "Tomato Cream Soup", "description": "Allergens: milk, celery", "dine_in_price": 0.00, "dish_type": "soup"},

            # Main Courses
            {"name": "Grilled Chicken Breast with Bacon, Rice, Carrot Salad", "description": "Allergens: celery", "dine_in_price": 3.60, "dish_type": "main_course"},
            {"name": "Shepherd's Pork Leg, Mashed Potatoes, Garnish", "description": "Allergens: gluten, milk, celery", "dine_in_price": 3.60, "dish_type": "main_course"},
            {"name": "Baked Potatoes with Vegetables, Beetroot and Cheese, Garnish", "description": "Allergens: gluten, milk, celery", "dine_in_price": 3.60, "dish_type": "main_course"},
            {"name": "Pizza Prosciutto, Salami, Olives, Onion, Cheese", "description": "Allergens: gluten, milk", "dine_in_price": 3.90, "dish_type": "main_course"},
            {"name": "Stuffed Baguette", "description": "Allergens: gluten, egg, milk, mustard", "dine_in_price": 1.50, "dish_type": "main_course"},
            {"name": "Fried Cheese with French Fries and Tartar Sauce", "description": "Allergens: milk, egg, gluten", "dine_in_price": 3.90, "dish_type": "main_course"},
            {"name": "Spaghetti Carbonara", "description": "Allergens: gluten, milk, egg", "dine_in_price": 3.80, "dish_type": "main_course"},
            {"name": "Roast Duck with Red Cabbage and Dumplings", "description": "Allergens: egg, gluten, milk", "dine_in_price": 4.20, "dish_type": "main_course"},
            {"name": "Chicken Caesar Salad", "description": "Allergens: egg, milk, fish, gluten", "dine_in_price": 3.50, "dish_type": "main_course"},

            # Sides
            {"name": "French Fries", "description": "Allergens: gluten", "dine_in_price": 1.50, "dish_type": "side_dish"},
            {"name": "Steamed Rice", "description": "", "dine_in_price": 1.20, "dish_type": "side_dish"},
            {"name": "Mashed Potatoes", "description": "Allergens: milk", "dine_in_price": 1.20, "dish_type": "side_dish"},
            {"name": "Boiled Potatoes", "description": "", "dine_in_price": 1.00, "dish_type": "side_dish"},
            {"name": "Grilled Vegetables", "description": "", "dine_in_price": 1.70, "dish_type": "side_dish"},
            {"name": "Coleslaw Salad", "description": "Allergens: egg, mustard", "dine_in_price": 1.00, "dish_type": "side_dish"},
            {"name": "Bread Roll", "description": "Allergens: gluten", "dine_in_price": 0.40, "dish_type": "side_dish"},

            # Desserts
            {"name": "Apple Pie", "description": "Allergens: egg, milk, gluten", "dine_in_price": 1.70, "dish_type": "main_course"},
            {"name": "Pancakes with Jam", "description": "Allergens: gluten, egg, milk", "dine_in_price": 1.70, "dish_type": "main_course"},

            # Drinks
            {"name": "Mineral Water", "description": "", "dine_in_price": 0.70, "dish_type": "drink"},
            {"name": "Orange Juice", "description": "", "dine_in_price": 1.20, "dish_type": "drink"},
            {"name": "Apple Juice", "description": "", "dine_in_price": 1.20, "dish_type": "drink"},
            {"name": "Cola", "description": "", "dine_in_price": 1.20, "dish_type": "drink"}
        ]

        dishes = [Dish.create_from_dict(d) for d in dishes_data]
        db.session.add_all(dishes)
        
        # Create Users
        user1 = AppUser.create_user(last_name='Student', first_name='One', email='student1@example.com', password='pass123', balance=25.50, role='student')
        user2 = AppUser.create_user(last_name='Faculty', first_name='One', email='faculty1@example.com', password='pass123', balance=40.00, role='staff')
        user3 = AppUser.create_user(last_name='Novák', first_name='Jakub', email='jakub.novak@example.com', password='pass123', balance=18.75, role='student')
        user4 = AppUser.create_user(last_name='Kováčová', first_name='Anna', email='anna.kovacova@example.com', password='pass123', balance=31.00, role='student')
        user5 = AppUser.create_user(last_name='Smith', first_name='John', email='john.smith@example.com', password='pass123', balance=0.00, role='staff')
        user6 = AppUser.create_user(last_name='Admin', first_name='Alice', email='admin@example.com', password='password', balance=100.00, role='admin')

        db.session.commit()
        print("  - Users, Cafeterias, and Dishes created successfully.")
        
        # --- Stage 2: Create dependent data (Menu for today) ---
        dish_map = {d.name: d for d in Dish.query.all()}
        menu_date = date(2025, 6, 28)
        
        main_menu = DailyMenu.create_menu(cafeteria_id=nova_menza.cafeteria_id, menu_date=menu_date)
        db.session.commit() # Commit to get menu_id
        
        # Après dish_map = {d.name: d for d in Dish.query.all()}
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Vegetable Soup with Vermicelli'].dish_id, dish_role='soup', display_order=0)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Grilled Chicken Breast with Bacon, Rice, Carrot Salad'].dish_id, dish_role='main_course', display_order=1)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map["Shepherd's Pork Leg, Mashed Potatoes, Garnish"].dish_id, dish_role='main_course', display_order=2)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Baked Potatoes with Vegetables, Beetroot and Cheese, Garnish'].dish_id, dish_role='main_course', display_order=3)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Pizza Prosciutto, Salami, Olives, Onion, Cheese'].dish_id, dish_role='main_course', display_order=5)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Stuffed Baguette'].dish_id, dish_role='main_course', display_order=8)

        
        db.session.commit()
        print(f"  - Menu for {menu_date} at '{nova_menza.name}' created successfully.")
        print("✅ Database population successful!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error populating database: {e}")
        # It's useful to see the full traceback for debugging
        import traceback
        traceback.print_exc()