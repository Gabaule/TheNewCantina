#!/usr/bin/env python3
"""
Flask REST API controller for The New Cantina application
"""

import os
import sys
from datetime import datetime
from decimal import Decimal
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db
from models.app_user import AppUser
from models.cafeteria import Cafeteria
from models.dish import Dish
from models.daily_menu import DailyMenu
# DailyMenuItem is removed
from models.reservation import Reservation
from models.order_item import OrderItem

# Create Flask app
app = Flask(__name__, template_folder='../templates')
# You should configure your app with a secret key, database URI, etc.
# app.config['SECRET_KEY'] = 'your-super-secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
# db.init_app(app)

# --- Authentication & Authorization Helpers ---

def api_require_login(f):
    """Decorator for API routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required. Please log in."}), 401
        
        user = AppUser.get_by_id(int(session["user_id"]))
        if not user:
             return jsonify({"error": "User not found. Please log in again."}), 401
        
        # Make the current user available to the route
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    return decorated_function

# --- API Routes (The Backend) ---

@app.route("/api/v1/health")
def health_check_api():
    """Health check endpoint for Docker and monitoring."""
    try:
        db.session.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route("/api/v1/login", methods=["POST"])
def api_login():
    """API endpoint for user login."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request format."}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    user = AppUser.get_by_email(email)
    if user and user.verify_password(password):
        session["user_id"] = user.user_id
        return jsonify(user.to_dict()), 200
    
    return jsonify({"error": "Invalid credentials."}), 401

@app.route("/api/v1/logout", methods=["POST"])
def api_logout():
    """API endpoint for user logout."""
    session.clear()
    return jsonify({"message": "You have been logged out successfully."}), 200

@app.route("/api/v1/cafeterias", methods=["GET"])
@api_require_login
def get_cafeterias(current_user):
    """Get a list of all available cafeterias."""
    cafeterias = Cafeteria.get_all_dicts()
    return jsonify(cafeterias), 200

@app.route("/api/v1/menu/<int:cafeteria_id>", methods=["GET"])
@api_require_login
def get_daily_menu(current_user, cafeteria_id):
    """Get the structured daily menu for a given cafeteria and date."""
    selected_date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    daily_menu = DailyMenu.query.filter_by(
        cafeteria_id=cafeteria_id,
        menu_date=selected_date
    ).first()
    
    if not daily_menu:
        return jsonify({"message": "No menu found for this date."}), 404
        
    return jsonify(daily_menu.to_dict()), 200

@app.route("/api/v1/reservations", methods=["POST"])
@api_require_login
def create_reservation(current_user):
    """Create a new meal reservation."""
    data = request.get_json()
    if not data or 'cafeteria_id' not in data or 'reservation_date' not in data or 'items' not in data:
        return jsonify({"error": "Missing required fields: cafeteria_id, reservation_date, items"}), 400

    # 1. Validate input and calculate total price
    total_price = Decimal("0.0")
    order_items_data = []
    for item in data.get('items', []):
        dish = Dish.get_by_id(item.get('dish_id'))
        if not dish or not dish.is_available:
            return jsonify({"error": f"Dish with ID {item.get('dish_id')} is invalid or unavailable."}), 400
        total_price += dish.dine_in_price
        order_items_data.append({'dish': dish, 'price': dish.dine_in_price})

    # 2. Check user balance
    if current_user.balance < total_price:
        return jsonify({
            "error": "Insufficient balance.",
            "current_balance": float(current_user.balance),
            "required_balance": float(total_price)
        }), 402 # Payment Required

    try:
        # 3. Create Reservation and OrderItems within a transaction
        new_reservation = Reservation(
            user_id=current_user.user_id,
            cafeteria_id=data['cafeteria_id'],
            reservation_datetime=datetime.strptime(data['reservation_date'], "%Y-%m-%d"),
            total=total_price,
            status='confirmed'
        )
        db.session.add(new_reservation)
        
        # This ensures the new_reservation gets an ID before we use it
        db.session.flush()

        for item_data in order_items_data:
            order_item = OrderItem(
                reservation_id=new_reservation.reservation_id,
                dish_id=item_data['dish'].dish_id,
                quantity=1, # Assuming quantity is always 1 per selection
                is_takeaway=False, # Add this to your frontend if needed
                applied_price=item_data['price']
            )
            db.session.add(order_item)
            
        # 4. Deduct balance from user
        current_user.balance -= total_price
        
        # 5. Commit transaction
        db.session.commit()

        return jsonify(new_reservation.to_dict()), 201 # Created
        
    except Exception as e:
        db.session.rollback()
        # In a real app, log the error `e`
        return jsonify({"error": "An internal error occurred while creating the reservation."}), 500

@app.route("/api/v1/reservations", methods=["GET"])
@api_require_login
def get_reservations(current_user):
    """Get the current user's reservation history."""
    reservations = Reservation.query.filter_by(user_id=current_user.user_id).order_by(Reservation.reservation_datetime.desc()).all()
    return jsonify([r.to_dict() for r in reservations]), 200


@app.route("/api/v1/user/balance", methods=["POST"])
@api_require_login
def add_to_balance(current_user):
    """Add funds to the user's balance."""
    data = request.get_json()
    try:
        amount = Decimal(data.get("amount", "0"))
        if 0.01 <= amount <= 500:
            current_user.balance += amount
            db.session.commit()
            return jsonify({
                "message": f"Successfully added ${amount:.2f} to your balance!",
                "new_balance": float(current_user.balance)
            }), 200
        else:
            return jsonify({"error": "Please enter an amount between $0.01 and $500.00"}), 400
    except Exception:
        return jsonify({"error": "Invalid amount entered. Please enter a valid number."}), 400


# --- Page-Serving Routes (The Frontend Shell) ---
# These routes now just render the main page.
# The data is loaded dynamically via JavaScript making calls to the API routes above.

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return redirect(url_for("dashboard_page"))

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout_page():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login_page"))

@app.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")

@app.route("/orders")
def orders_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("orders.html")

@app.route("/balance")
def balance_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    # Pass user to template to display name and current balance initially
    user = AppUser.get_by_id(session['user_id'])
    return render_template("balance.html", user=user)


# --- Error Handlers (Context-Aware) ---
def handle_error(error, code):
    """Generic error handler that returns JSON for API routes and HTML for others."""
    if request.path.startswith('/api/'):
        return jsonify(error=str(error.description)), code
    # For web pages, render the appropriate HTML error template
    template = "500.html" if code == 500 else "404.html"
    return render_template(template), code

@app.errorhandler(404)
def not_found(error):
    return handle_error(error, 404)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() # Ensure session is clean after an internal error
    return handle_error(error, 500)