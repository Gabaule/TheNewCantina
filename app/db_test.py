#!/usr/bin/env python3
"""
Quick database connection test for the canteen management system
Enhanced with proper database waiting functionality
"""

import time
import sys
import logging
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import psycopg2
from models.base_model import db
from models.user import User
from models.canteen import Canteen
from models.dish import Dish
from models.order import Order
from models.order_detail import OrderDetail
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def wait_for_database(database_url, max_retries=30, retry_interval=2):
    """
    Wait for database to become available with exponential backoff
    
    Args:
        database_url: PostgreSQL connection URL
        max_retries: Maximum number of connection attempts
        retry_interval: Initial wait time between retries (seconds)
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    logger.info(f"🔄 Waiting for database to become available...")
    logger.info(f"   Max retries: {max_retries}")
    logger.info(f"   Retry interval: {retry_interval}s")
    
    for attempt in range(1, max_retries + 1):
        try:
            # Try to create a simple connection
            engine = create_engine(database_url, pool_pre_ping=True)
            
            # Test the connection with a simple query
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
            
            logger.info(f"✅ Database connection successful on attempt {attempt}!")
            engine.dispose()  # Clean up the test engine
            return True
            
        except (OperationalError, psycopg2.OperationalError) as e:
            if attempt == max_retries:
                logger.error(f"❌ Failed to connect to database after {max_retries} attempts")
                logger.error(f"   Last error: {str(e)}")
                return False
            
            # Calculate wait time with exponential backoff (max 10 seconds)
            wait_time = min(retry_interval * (1.5 ** (attempt - 1)), 10)
            
            logger.warning(f"⏳ Attempt {attempt}/{max_retries} failed. Retrying in {wait_time:.1f}s...")
            logger.warning(f"   Error: {str(e).split(chr(10))[0]}")  # First line only
            
            time.sleep(wait_time)
            
        except Exception as e:
            logger.error(f"❌ Unexpected error during database connection: {str(e)}")
            return False
    
    return False

def wait_for_database_simple(database_url, timeout=60):
    """
    Simple database wait with timeout
    
    Args:
        database_url: PostgreSQL connection URL
        timeout: Maximum time to wait in seconds
    
    Returns:
        bool: True if connection successful, False if timeout
    """
    logger.info(f"🔄 Waiting for database (timeout: {timeout}s)...")
    
    start_time = time.time()
    attempt = 0
    
    while time.time() - start_time < timeout:
        attempt += 1
        try:
            engine = create_engine(database_url, pool_pre_ping=True)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            logger.info(f"✅ Database ready after {time.time() - start_time:.1f}s (attempt {attempt})")
            engine.dispose()
            return True
            
        except Exception:
            elapsed = time.time() - start_time
            remaining = timeout - elapsed
            
            if remaining > 0:
                logger.info(f"⏳ Database not ready... {remaining:.0f}s remaining (attempt {attempt})")
                time.sleep(2)
            
    logger.error(f"❌ Database connection timeout after {timeout}s")
    return False

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
    
    database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'  # Change in production
    
    # Wait for database before initializing SQLAlchemy
    print("🔄 Waiting for database to become available...")
    if not wait_for_database(database_url):
        print("❌ Failed to establish database connection. Exiting...")
        sys.exit(1)
    
    # Initialize database
    db.init_app(app)
    
    return app

def create_app_with_health_check():
    """Create Flask application with health check functionality"""
    app = Flask(__name__)
    
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'postgres-db')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'TheNewCantina')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    # Add health check route
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db.engine.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}, 200
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}, 503
    
    return app, database_url

def test_database_connection():
    """Test database connection and basic operations"""
    app = create_app()
    
    with app.app_context():
        try:
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

# Alternative: Docker Compose health check approach
def create_docker_compose_healthcheck():
    """
    Returns a health check command for docker-compose.yml
    This approach uses Docker's built-in health checking
    """
    return """
# Add this to your docker-compose.yml for the postgres service:
postgres-db:
  image: postgres:13
  environment:
    POSTGRES_DB: TheNewCantina
    POSTGRES_USER: admin
    POSTGRES_PASSWORD: password
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U admin -d TheNewCantina"]
    interval: 5s
    timeout: 5s
    retries: 5
    start_period: 10s

# And for your app service:
canteen-app:
  build: .
  depends_on:
    postgres-db:
      condition: service_healthy  # Wait for DB to be healthy
  environment:
    DB_HOST: postgres-db
"""

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