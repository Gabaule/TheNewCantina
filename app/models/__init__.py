from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to ensure they're registered with SQLAlchemy
from .app_user import AppUser
from .cafeteria import Cafeteria
from .dish import Dish
from .daily_menu import DailyMenu
from .daily_menu_item import DailyMenuItem
from .reservation import Reservation
from .order_item import OrderItem

__all__ = [
    'db',
    'AppUser', 
    'Cafeteria', 
    'Dish', 
    'DailyMenu', 
    'DailyMenuItem', 
    'Reservation', 
    'OrderItem'
]