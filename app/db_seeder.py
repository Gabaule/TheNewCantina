import os
import sys
from datetime import date, datetime

# Add parent directory to path to allow model imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
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
        cafeteria1 = Cafeteria.create_cafeteria(name='Main University Cafeteria', address='Campus A, Main Road 1', phone='+421 41 513 4001')
        cafeteria2 = Cafeteria.create_cafeteria(name='Faculty of Science Cafeteria', address='Science Building, 2nd Floor', phone='+421 41 513 4201')
        
        dishes_data = [
            {'name': 'Schnitzel with Potato Salad', 'description': 'Breaded pork schnitzel served with classic potato salad', 'dine_in_price': 5.80, 'dish_type': 'main_course'},
            {'name': 'Chicken Breast with Rice', 'description': 'Grilled chicken breast, rice, and steamed vegetables', 'dine_in_price': 5.20, 'dish_type': 'main_course'},
            {'name': 'Goulash with Dumplings', 'description': 'Hearty beef goulash with bread dumplings', 'dine_in_price': 4.90, 'dish_type': 'main_course'},
            {'name': 'French Fries', 'description': 'Crispy golden french fries', 'dine_in_price': 2.30, 'dish_type': 'side_dish'},
            {'name': 'Mixed Salad', 'description': 'Fresh seasonal salad with a light vinaigrette', 'dine_in_price': 2.80, 'dish_type': 'side_dish'},
            {'name': 'Bread Roll', 'description': 'Freshly baked bread roll', 'dine_in_price': 0.60, 'dish_type': 'side_dish'},
            {'name': 'Chicken Soup', 'description': 'Clear chicken broth with noodles and vegetables', 'dine_in_price': 1.80, 'dish_type': 'soup'},
            {'name': 'Mineral Water', 'description': 'Sparkling or still mineral water', 'dine_in_price': 1.10, 'dish_type': 'drink'}
        ]
        dishes = [Dish.create_from_dict(d) for d in dishes_data]
        db.session.add_all(dishes)
        
        user1 = AppUser.create_user(last_name='Student', first_name='One', email='student1@example.com', password='pass123', balance=25.50, role='student')
        user2 = AppUser.create_user(last_name='Faculty', first_name='One', email='faculty1@example.com', password='pass123', balance=40.00, role='staff')
        user3 = AppUser.create_user(last_name='Novák', first_name='Jakub', email='jakub.novak@example.com', password='pass123', balance=18.75, role='student')
        user4 = AppUser.create_user(last_name='Kováčová', first_name='Anna', email='anna.kovacova@example.com', password='pass123', balance=31.00, role='student')
        user5 = AppUser.create_user(last_name='Smith', first_name='John', email='john.smith@example.com', password='pass123', balance=0.00, role='staff')
        user6 = AppUser.create_user(last_name='Admin', first_name='Alice', email='admin@example.com', password='admin_pass', balance=100.00, role='admin')

        db.session.commit()
        print("  - Users, Cafeterias, and Dishes created successfully.")
        
        # --- Stage 2: Create dependent data (Menus, Reservations) ---
        dish_map = {d.name: d for d in Dish.query.all()}
        menu_date = date(2025, 6, 25)
        
        main_menu = DailyMenu.create_menu(cafeteria_id=cafeteria1.cafeteria_id, menu_date=menu_date)
        db.session.commit() # Commit to get menu_id
        
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Schnitzel with Potato Salad'].dish_id, dish_role='main_course', display_order=1)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Chicken Breast with Rice'].dish_id, dish_role='main_course', display_order=2)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Goulash with Dumplings'].dish_id, dish_role='main_course', display_order=3)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['French Fries'].dish_id, dish_role='side_dish', display_order=1)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Mixed Salad'].dish_id, dish_role='side_dish', display_order=2)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Bread Roll'].dish_id, dish_role='side_dish', display_order=3)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Chicken Soup'].dish_id, dish_role='soup', display_order=1)
        DailyMenuItem.create_menu_item(menu_id=main_menu.menu_id, dish_id=dish_map['Mineral Water'].dish_id, dish_role='drink', display_order=1)
        
        res1 = Reservation.create_reservation(user_id=user3.user_id, cafeteria_id=cafeteria1.cafeteria_id, reservation_datetime=datetime(2025, 6, 25, 12, 0, 0), total=9.90, status='completed')
        res2 = Reservation.create_reservation(user_id=user4.user_id, cafeteria_id=cafeteria1.cafeteria_id, reservation_datetime=datetime(2025, 6, 25, 12, 30, 0), total=9.10, status='pending')
        res3 = Reservation.create_reservation(user_id=user5.user_id, cafeteria_id=cafeteria1.cafeteria_id, reservation_datetime=datetime(2025, 6, 25, 13, 0, 0), total=6.60, status='completed')
        
        db.session.flush() # Flush to assign IDs to reservations before creating order items

        OrderItem.create_order_item(reservation_id=res1.reservation_id, dish_id=dish_map['Schnitzel with Potato Salad'].dish_id, quantity=1, is_takeaway=False, applied_price=5.80)
        OrderItem.create_order_item(reservation_id=res1.reservation_id, dish_id=dish_map['Chicken Soup'].dish_id, quantity=1, is_takeaway=False, applied_price=1.80)
        OrderItem.create_order_item(reservation_id=res1.reservation_id, dish_id=dish_map['French Fries'].dish_id, quantity=1, is_takeaway=False, applied_price=2.30)

        OrderItem.create_order_item(reservation_id=res2.reservation_id, dish_id=dish_map['Chicken Breast with Rice'].dish_id, quantity=1, is_takeaway=True, applied_price=5.20)
        OrderItem.create_order_item(reservation_id=res2.reservation_id, dish_id=dish_map['Mixed Salad'].dish_id, quantity=1, is_takeaway=True, applied_price=2.80)
        OrderItem.create_order_item(reservation_id=res2.reservation_id, dish_id=dish_map['Mineral Water'].dish_id, quantity=1, is_takeaway=True, applied_price=1.10)
        
        OrderItem.create_order_item(reservation_id=res3.reservation_id, dish_id=dish_map['Goulash with Dumplings'].dish_id, quantity=1, is_takeaway=False, applied_price=4.90)
        OrderItem.create_order_item(reservation_id=res3.reservation_id, dish_id=dish_map['Bread Roll'].dish_id, quantity=1, is_takeaway=False, applied_price=0.60)
        OrderItem.create_order_item(reservation_id=res3.reservation_id, dish_id=dish_map['Mineral Water'].dish_id, quantity=1, is_takeaway=False, applied_price=1.10)
        
        db.session.commit()
        print("  - Dependent data (Menus, Reservations, etc.) created successfully.")
        print("✅ Database population successful!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error populating database: {e}")
        # It's useful to see the full traceback for debugging
        import traceback
        traceback.print_exc()