#!/usr/bin/env python3
"""
Quick database connection test for the canteen management system
"""

import time
from flask import Flask
from models.base_model import db
from models.user import User
from models.canteen import Canteen
from models.dish import Dish
from models.order import Order
from models.order_detail import OrderDetail
import os
from datetime import datetime


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    # Database configuration
    # Update these values according to your PostgreSQL setup
    DB_HOST = os.getenv('DB_HOST', 'postgres-db')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'TheNewCantina')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'  # Change in production
    
    # Initialize database
    db.init_app(app)
    
    return app

def test_database_connection():
    """Test database connection and basic operations"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Attente de 10 secondes...")
            for i in range(10, 0, -1):
                print(f"{i} secondes restantes...")
                time.sleep(1)
            print("Terminé !")
            print("🔄 Testing database connection...")
            
            # Test 1: Check if we can connect
            db.engine.connect()
            print("✅ Database connection successful!")
            
            # Test 2: Check if tables exist (basic query)
            user_count = User.count()
            canteen_count = Canteen.count()
            dish_count = Dish.count()
            order_count = Order.count()
            
            print(f"📊 Database Statistics:")
            print(f"   - Users: {user_count}")
            print(f"   - Canteens: {canteen_count}")
            print(f"   - Dishes: {dish_count}")
            print(f"   - Orders: {order_count}")
            
            # Test 3: Try to fetch some sample data
            print("\n🔍 Sample Data:")
            
            # Get first user
            first_user = User.query.first()
            if first_user:
                print(f"   - First User: {first_user.full_name} ({first_user.email})")
                print(f"   - Balance: €{first_user.balance_float:.2f}")
            
            # Get first canteen
            first_canteen = Canteen.query.first()
            if first_canteen:
                print(f"   - First Canteen: {first_canteen.name}")
            
            # Get available dishes count
            available_dishes = len(Dish.get_available())
            print(f"   - Available Dishes: {available_dishes}")
            
            # Get recent orders
            recent_orders = Order.query.order_by(Order.order_date.desc()).limit(3).all()
            print(f"   - Recent Orders: {len(recent_orders)}")
            
            # Test 4: Try a simple query with joins
            if recent_orders:
                print("\n📋 Recent Order Details:")
                for order in recent_orders:
                    print(f"   - Order #{order.order_id}: €{order.total} ({order.status})")
                    print(f"     User: {order.user.full_name if order.user else 'Unknown'}")
                    print(f"     Canteen: {order.canteen.name if order.canteen else 'Unknown'}")
                    print(f"     Date: {order.order_date.strftime('%Y-%m-%d %H:%M')}")
                    print(f"     Items: {len(order.order_details)}")
                    print()
            
            print("🎉 All database tests passed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            return False

def test_model_operations():
    """Test basic model operations"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🧪 Testing Model Operations...")
            
            # Test User operations
            print("   Testing User model...")
            test_user = User.get_by_email('jakub.novak@stud.uniza.sk')
            if test_user:
                print(f"   ✅ Found user: {test_user.full_name}")
                print(f"      Balance: €{test_user.balance_float:.2f}")
                
                # Test balance check
                can_spend_5 = test_user.has_sufficient_balance(5.00)
                print(f"      Can spend €5.00: {can_spend_5}")
            
            # Test Dish operations
            print("   Testing Dish model...")
            available_dishes = Dish.get_available()
            if available_dishes:
                dish = available_dishes[0]
                print(f"   ✅ Sample dish: {dish.name}")
                print(f"      Dine-in: €{dish.dine_in_price}, Takeaway: €{dish.takeaway_price}")
                print(f"      Available: {dish.is_available}")
            
            # Test search functionality
            print("   Testing search functionality...")
            search_results = User.search_users("jakub", limit=3)
            print(f"   ✅ Search results for 'jakub': {len(search_results)} users")
            
            dish_search = Dish.search_by_name("schnitzel")
            print(f"   ✅ Dish search for 'schnitzel': {len(dish_search)} dishes")
            
            print("✅ Model operations test completed!")
            
        except Exception as e:
            print(f"❌ Model operations test failed: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Starting Canteen Management System Database Test\n")
    
    # Test database connection
    connection_success = test_database_connection()
    
    if connection_success:
        # Test model operations
        test_model_operations()
        print("\n🎯 Quick Test Summary:")
        print("   - Database connection: ✅")
        print("   - Model operations: ✅")
        print("   - Ready for development! 🚀")
    else:
        print("\n❌ Database connection failed. Please check:")
        print("   1. PostgreSQL server is running")
        print("   2. Database credentials are correct")
        print("   3. Database and tables exist")
        print("   4. Required Python packages are installed:")
        print("      pip install flask sqlalchemy psycopg2-binary")