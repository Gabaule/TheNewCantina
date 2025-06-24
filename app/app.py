from flask import Flask
from models import db
from controller.controller import app as controller_app
import os

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Database configuration - matching Docker Compose settings
    DB_HOST = os.getenv('DB_HOST', 'postgres-db')  # Docker service name
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'TheNewCantina')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    
    database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretdevstring')
    
    # Initialize database
    db.init_app(app)
    
    # Register routes from controller
    app.register_blueprint(controller_app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5045)