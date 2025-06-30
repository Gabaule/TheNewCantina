# File: app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Import tes modèles ici pour qu’ils soient connus de SQLAlchemy
from .app_user import AppUser
from .cafeteria import Cafeteria
from .dish import Dish
from .daily_menu import DailyMenu
from .daily_menu_item import DailyMenuItem
from .reservation import Reservation
from .order_item import OrderItem