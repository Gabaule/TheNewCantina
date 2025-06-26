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
from sqlalchemy import text

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
        
        # --- START DEBUG LOGGING ---
        print(f"--- Login attempt ---")
        print(f"Received email: '{email}'")
        print(f"Received password: '{password}'")

        user = AppUser.get_by_email(email)
        
        if not user:
            print("DEBUG: User not found in database.")
        else:
            print(f"DEBUG: User found: {user.email}, Role: {user.role}")
            password_is_valid = user.verify_password(password)
            print(f"DEBUG: Password verification result: {password_is_valid}")
            if password_is_valid:
                session["user_id"] = user.user_id
                flash(f"Welcome back, {user.first_name}!", "success")
                print("--- Login successful, redirecting. ---")
                return redirect(url_for("dashboard"))

        # This part only runs if login fails
        print("--- Login failed. Rendering login page with error. ---")
        flash("Invalid credentials. Please try again.", "error")
        return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    user = get_current_user()
    user_name = f"{user.first_name} {user.last_name}" if user else "User"
    session.clear()
    flash(f"Goodbye, {user_name}! You've been logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@app.route("/dashboard/<int:cafeteria_id>")
def dashboard(cafeteria_id=None):
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get all cafeterias
    cafeterias = Cafeteria.query.all()
    
    # Get current cafeteria
    if cafeteria_id:
        current_cafeteria = Cafeteria.query.get_or_404(cafeteria_id)
    else:
        current_cafeteria = cafeterias[0] if cafeterias else None
        if current_cafeteria:
            return redirect(url_for("dashboard", cafeteria_id=current_cafeteria.cafeteria_id))
    
    # Get selected date from query params or use today
    selected_date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    # Get menu for the selected date and cafeteria
    menu_items = []
    if current_cafeteria:
        daily_menu = DailyMenu.query.filter_by(
            cafeteria_id=current_cafeteria.cafeteria_id,
            menu_date=selected_date
        ).first()
        
        if daily_menu:
            menu_items = db.session.query(Dish, DailyMenuItem).join(
                DailyMenuItem, Dish.dish_id == DailyMenuItem.dish_id
            ).filter(
                DailyMenuItem.menu_id == daily_menu.menu_id
            ).order_by(DailyMenuItem.display_order).all()
    
    return render_template(
        "dashboard.html",
        cafeterias=cafeterias,
        current_cafeteria=current_cafeteria,
        menu=menu_items,
        user=user,
        selected_date=selected_date,
    )

@app.route("/balance", methods=["GET", "POST"])
def balance():
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))
            if 0.01 <= amount <= 500:
                user.balance += amount
                db.session.commit()
                flash(f"Successfully added ${amount:.2f} to your balance!", "success")
                return redirect(url_for("balance"))
            else:
                flash("Please enter an amount between $0.01 and $500.00", "error")
        except (ValueError, TypeError):
            flash("Invalid amount entered. Please enter a valid number.", "error")
    
    return render_template("balance.html", user=user)

@app.route("/orders")
def orders():
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get user's reservations/orders
    reservations = Reservation.get_by_user(user.user_id)
    
    # Filter by month if requested
    selected_month = request.args.get("month")
    selected_month_name = "All Time"
    
    if selected_month:
        try:
            year, month = map(int, selected_month.split("-"))
            reservations = [
                r for r in reservations 
                if r.reservation_datetime.year == year and r.reservation_datetime.month == month
            ]
            month_names = ["", "January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
            selected_month_name = f"{month_names[month]} {year}"
        except (ValueError, IndexError):
            selected_month = None
    
    # Generate monthly summary
    monthly_summary = {}
    if reservations:
        from collections import defaultdict
        monthly_totals = defaultdict(lambda: {"count": 0, "total": 0.0})
        
        for reservation in reservations:
            month_key = f"{reservation.reservation_datetime.year}-{reservation.reservation_datetime.month:02d}"
            monthly_totals[month_key]["count"] += 1
            monthly_totals[month_key]["total"] += float(reservation.total)
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        for month_key, data in monthly_totals.items():
            year, month = map(int, month_key.split("-"))
            monthly_summary[month_key] = {
                "month_name": f"{month_names[month]} {year}",
                "count": data["count"],
                "total": data["total"]
            }
    
    return render_template(
        "orders.html", 
        user=user,
        orders=reservations,
        selected_month=selected_month,
        selected_month_name=selected_month_name,
        monthly_summary=monthly_summary
    )

@app.route("/api/menu/<int:cafeteria_id>")
def api_menu(cafeteria_id):
    """API endpoint to get menu for a specific cafeteria"""
    auth_check = require_login()
    if auth_check:
        return jsonify({"error": "Authentication required"}), 401
    
    selected_date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    # Get menu for the selected date and cafeteria
    daily_menu = DailyMenu.query.filter_by(
        cafeteria_id=cafeteria_id,
        menu_date=selected_date
    ).first()
    
    if not daily_menu:
        return jsonify({"menu": []})
    
    menu_items = db.session.query(Dish, DailyMenuItem).join(
        DailyMenuItem, Dish.dish_id == DailyMenuItem.dish_id
    ).filter(
        DailyMenuItem.menu_id == daily_menu.menu_id
    ).order_by(DailyMenuItem.display_order).all()
    
    menu_data = []
    for dish, menu_item in menu_items:
        menu_data.append({
            "dish_id": dish.dish_id,
            "name": dish.name,
            "description": dish.description,
            "price": float(dish.dine_in_price),
            "dish_type": dish.dish_type,
            "role": menu_item.dish_role
        })
    
    return jsonify({"menu": menu_data})

@app.route("/health")
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Test database connection
        db.session.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}, 200
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