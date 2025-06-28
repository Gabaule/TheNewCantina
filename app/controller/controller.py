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

# Corrected and consolidated imports
from models import db
from models.app_user import AppUser
from models.cafeteria import Cafeteria
from models.dish import Dish
from models.daily_menu import DailyMenu
from models.daily_menu_item import DailyMenuItem  # FIXED: This was missing
from models.reservation import Reservation
from models.order_item import OrderItem

# Create Flask app
app = Flask(__name__, template_folder='../templates')
# App configuration (secret key, DB URI) is handled in app.py

# --- Authentication & Authorization Helpers (FIXED) ---

def get_current_user():
    """Helper to get the currently logged-in user object from session."""
    if "user_id" in session:
        return AppUser.get_by_id(session["user_id"])
    return None

def require_login():
    """Helper function to protect web pages, redirects if not logged in."""
    if "user_id" not in session:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("login"))
    return None

def admin_web_required(f):
    """Decorator for web pages that require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_check = require_login()
        if auth_check:
            return auth_check

        user = get_current_user()
        if not user:
            flash("User not found, please log in again.", "error")
            session.clear()
            return redirect(url_for("login"))

        if user.role != "admin":
            flash("You do not have permission to access this page.", "error")
            # Redirect non-admins away to their own dashboard
            return redirect(url_for("dashboard"))
        
        # Pass the user object to the decorated function
        return f(current_user=user, *args, **kwargs)
    return decorated_function

def api_require_login(f):
    """Decorator for API routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required. Please log in."}), 401
        
        user = get_current_user()
        if not user:
            session.clear()
            return jsonify({"error": "User not found. Please log in again."}), 401
        
        # Pass the user object to the decorated function
        return f(current_user=user, *args, **kwargs)
    return decorated_function


# --- Core Page Routes (Consolidated and Fixed) ---

@app.route("/")
def index():
    if "user_id" in session:
        user = get_current_user()
        if user and user.role == 'admin':
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")

        user = AppUser.get_by_email(email)
        
        if user and user.verify_password(password):
            session["user_id"] = user.user_id
            session.permanent = True
            flash(f"Welcome back, {user.first_name}!", "success")
            
            # Redirect admin to admin dashboard, others to regular dashboard
            if user.role == 'admin':
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "error")
            return render_template("login.html")
    
    # For GET request
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
    if user.role == 'admin':
        # Don't let admins see the student dashboard
        return redirect(url_for('admin_dashboard'))
    
    cafeterias = Cafeteria.query.all()
    if not cafeterias:
        flash("No cafeterias have been configured in the system.", "warning")
        return render_template("dashboard.html", user=user, cafeterias=[], current_cafeteria=None, menu=[])

    if cafeteria_id:
        current_cafeteria = Cafeteria.query.get_or_404(cafeteria_id)
    else:
        # If no cafeteria is specified, redirect to the first one
        current_cafeteria = cafeterias[0]
        return redirect(url_for("dashboard", cafeteria_id=current_cafeteria.cafeteria_id))
    
    selected_date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date = datetime.now().date()

    menu_items = []
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
        # FIXED: Removed space in variable name
        current_cafeteria=current_cafeteria,
        menu=menu_items,
        user=user,
        selected_date=selected_date.strftime("%Y-%m-%d"),
    )

@app.route("/balance", methods=["GET", "POST"])
def balance():
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    user = get_current_user()
    
    if request.method == "POST":
        try:
            amount = Decimal(request.form.get("amount", "0"))
            if Decimal("0.01") <= amount <= Decimal("500.00"):
                user.balance += amount
                db.session.commit()
                flash(f"Successfully added ${amount:.2f} to your balance!", "success")
                return redirect(url_for("balance"))
            else:
                flash("Please enter an amount between $0.01 and $500.00", "error")
        except Exception:
            flash("Invalid amount entered. Please enter a valid number.", "error")
    
    return render_template("balance.html", user=user)

@app.route("/orders")
def orders():
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    user = get_current_user()
    
    # Base query for user's reservations
    reservations_query = Reservation.query.filter_by(user_id=user.user_id).order_by(Reservation.reservation_datetime.desc())
    
    selected_month = request.args.get("month")
    selected_month_name = "All Time"
    
    # Filter reservations if a month is selected
    if selected_month:
        try:
            year, month = map(int, selected_month.split("-"))
            reservations = reservations_query.filter(
                db.extract('year', Reservation.reservation_datetime) == year,
                db.extract('month', Reservation.reservation_datetime) == month
            ).all()
            selected_month_name = datetime(year, month, 1).strftime("%B %Y")
        except (ValueError, IndexError):
            selected_month = None
            reservations = reservations_query.all()
    else:
        reservations = reservations_query.all()
    
    # Generate monthly summary from all of the user's reservations
    from collections import defaultdict
    monthly_totals = defaultdict(lambda: {"count": 0, "total": Decimal("0.0")})
    
    for reservation in reservations_query.all():
        month_key = reservation.reservation_datetime.strftime("%Y-%m")
        monthly_totals[month_key]["count"] += 1
        monthly_totals[month_key]["total"] += reservation.total
    
    monthly_summary = {}
    for month_key, data in sorted(monthly_totals.items(), reverse=True):
        year, month = map(int, month_key.split("-"))
        monthly_summary[month_key] = {
            "month_name": datetime(year, month, 1).strftime("%B %Y"),
            "count": data["count"],
            "total": float(data["total"])
        }
    
    return render_template(
        "orders.html", 
        user=user,
        orders=reservations,
        selected_month=selected_month,
        selected_month_name=selected_month_name,
        monthly_summary=monthly_summary
    )


# --- Admin Routes ---

@app.route("/admin/dashboard")
@admin_web_required
def admin_dashboard(current_user):
    cafeterias = Cafeteria.query.order_by(Cafeteria.name).all()
    dishes = Dish.query.order_by(Dish.name).all()
    categorized_dishes = {
        'soup': [d for d in dishes if d.dish_type == 'soup'],
        'main_course': [d for d in dishes if d.dish_type == 'main_course'],
        'side_dish': [d for d in dishes if d.dish_type == 'side_dish'],
        'drink': [d for d in dishes if d.dish_type == 'drink'],
    }
    return render_template(
        "admin/dashboard.html", 
        user=current_user, 
        cafeterias=cafeterias, 
        dishes=categorized_dishes,
        now=datetime.now()
    )

@app.route("/admin/users")
@admin_web_required
def admin_users(current_user):
    all_users = AppUser.query.order_by(AppUser.last_name, AppUser.first_name).all()
    return render_template("admin/users.html", user=current_user, users=all_users)

@app.route("/admin/menu", methods=['POST'])
@admin_web_required
def create_admin_menu(current_user):
    try:
        cafeteria_id = request.form.get('cafeteria_id')
        menu_date_str = request.form.get('menu_date')
        dish_ids = request.form.getlist('dish_ids')

        if not all([cafeteria_id, menu_date_str, dish_ids]):
            flash("All fields are required to create a menu.", "error")
            return redirect(url_for('admin_dashboard'))

        menu_date = datetime.strptime(menu_date_str, "%Y-%m-%d").date()
        
        existing_menu = DailyMenu.query.filter_by(cafeteria_id=cafeteria_id, menu_date=menu_date).first()
        if existing_menu:
            flash(f"A menu for this cafeteria on {menu_date_str} already exists. Please delete it first if you want to replace it.", "error")
            return redirect(url_for('admin_dashboard'))
        
        new_menu = DailyMenu.create_menu(cafeteria_id=cafeteria_id, menu_date=menu_date)
        db.session.flush()

        dishes = Dish.query.filter(Dish.dish_id.in_(dish_ids)).all()
        for dish in dishes:
            DailyMenuItem.create_menu_item(
                menu_id=new_menu.menu_id,
                dish_id=dish.dish_id,
                dish_role=dish.dish_type
            )

        db.session.commit()
        flash(f"Menu for {menu_date_str} created successfully!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while creating the menu: {e}", "error")

    return redirect(url_for('admin_dashboard'))


# --- API Routes ---

@app.route("/api/menu/<int:cafeteria_id>")
@api_require_login
def api_menu(current_user, cafeteria_id):
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
        return jsonify({"menu": []})
    
    menu_items = db.session.query(Dish, DailyMenuItem).join(
        DailyMenuItem, Dish.dish_id == DailyMenuItem.dish_id
    ).filter(
        DailyMenuItem.menu_id == daily_menu.menu_id
    ).order_by(DailyMenuItem.display_order).all()
    
    menu_data = [
        {
            "dish_id": dish.dish_id,
            "name": dish.name,
            "description": dish.description,
            "price": float(dish.dine_in_price),
            "dish_type": dish.dish_type,
            "role": menu_item.dish_role
        } for dish, menu_item in menu_items
    ]
    return jsonify({"menu": menu_data})

@app.route("/health")
def health_check():
    """Health check endpoint for Docker"""
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 503

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
    if not data:
        return jsonify({"error": "Invalid request body."}), 400
    try:
        amount = Decimal(data.get("amount", "0"))
        if Decimal("0.01") <= amount <= Decimal("500.00"):
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


# --- Error Handlers (Context-Aware) ---
def handle_error(error, code):
    """Generic error handler that returns JSON for API routes and HTML for others."""
    if request.path.startswith('/api/'):
        error_message = getattr(error, 'description', str(error))
        return jsonify(error=error_message), code
    
    template = "500.html" if code >= 500 else "404.html"
    return render_template(template, error=error), code

@app.errorhandler(404)
def not_found(error):
    return handle_error(error, 404)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() 
    return handle_error(error, 500)