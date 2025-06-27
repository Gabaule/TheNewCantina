#!/usr/bin/env python3
"""
Main application entry point for The New Cantina
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from controller
from controller.controller import app
from models import db
from db_seeder import populate_database_if_empty

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'postgres-db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'TheNewCantina')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
print(f"🔑 [DEBUG] Secret Key is set. Value: {''.join('*' for char in app.secret_key)}")

# Initialize database
db.init_app(app)

# Create tables and populate with initial data if database is empty
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created/verified successfully!")
        
        # Call the separated seeder function
        populate_database_if_empty()

    except Exception as e:
        print(f"❌ Error during app initialization: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5045)