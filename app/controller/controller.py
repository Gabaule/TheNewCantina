#!/usr/bin/env python3
"""
Flask Main Controller for The New Cantina application
Handles Web Page routes, authentication, and blueprint registration.
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

# Model imports
from models import db, AppUser, Cafeteria, Dish, DailyMenu, DailyMenuItem, Reservation

# --- Util/Auth Helper Imports ---
# MODIFIÉ ICI : On importe depuis le nouveau fichier auth.py
from .auth import get_current_user, require_login

# --- Blueprint Imports ---
from .user_controller import user_bp
from .dish_controller import dish_bp
from .cafeteria_controller import cafeteria_bp
from .reservation_controller import reservation_bp
from .daily_menu_controller import daily_menu_bp
from .daily_menu_item_controller import daily_menu_item_bp
from .order_item_controller import order_item_bp

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


# --- Core Page Routes ---

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
        print("\n--- [DEBUG] Attempting Login ---")
        email = request.form.get("username")
        password = request.form.get("password")
        print(f"[DEBUG] Form Data -> Email: '{email}', Password: {'*' * len(password)}")

        if not email or not password:
            print("[DEBUG] ❌ Email or password missing from form.")
            flash("Email et mot de passe sont requis.", "error")
            return render_template("login.html")

        user = AppUser.get_by_email(email)
        
        if user and user.verify_password(password):
            print(f"[DEBUG] ✅ User found in DB: {user.first_name} (ID: {user.user_id})")
            session["user_id"] = user.user_id
            session.permanent = True
            
            # Redirect admin to admin dashboard, others to regular dashboard
            if user.role == 'admin':
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            flash("Identifiants invalides. Veuillez réessayer.", "error")
            return render_template("login.html")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@app.route("/dashboard/<int:cafeteria_id>")
def dashboard(cafeteria_id=None):
    # La fonction require_login est maintenant importée de auth.py
    auth_check = require_login() 
    if auth_check: return auth_check
    
    user = get_current_user()
    if user.role == 'admin':
        # Don't let admins see the student dashboard
        return redirect(url_for('admin_dashboard'))
    
    cafeterias = Cafeteria.query.all()
    if not cafeterias:
        flash("Aucune cafétéria n'a été configurée dans le système.", "warning")
        return render_template("dashboard.html", user=user, cafeterias=[], current_cafeteria=None, menu=[])

    if cafeteria_id:
        current_cafeteria = Cafeteria.query.get_or_404(cafeteria_id)
    else:
        current_cafeteria = cafeterias[0]
        return redirect(url_for("dashboard", cafeteria_id=current_cafeteria.cafeteria_id))
    
    selected_date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date = datetime.now().date()

    daily_menu = DailyMenu.query.filter_by(
        cafeteria_id=current_cafeteria.cafeteria_id, menu_date=selected_date
    ).first()
    
    menu_items = []
    if daily_menu:
        menu_items = db.session.query(Dish, DailyMenuItem).join(
            DailyMenuItem, Dish.dish_id == DailyMenuItem.dish_id
        ).filter(
            DailyMenuItem.menu_id == daily_menu.menu_id
        ).order_by(DailyMenuItem.display_order).all()
    
    return render_template(
        "dashboard.html", cafeterias=cafeterias, current_cafeteria=current_cafeteria,
        menu=menu_items, user=user, selected_date=selected_date.strftime("%Y-%m-%d")
    )

@app.route("/balance", methods=["GET", "POST"])
def balance():
    auth_check = require_login()
    if auth_check: return auth_check
    
    user = get_current_user()
    
    if request.method == "POST":
        try:
            amount = Decimal(request.form.get("amount", "0"))
            if Decimal("0.01") <= amount <= Decimal("500.00"):
                user.balance += amount
                db.session.commit()
                return redirect(url_for("balance"))
            else:
                flash("Veuillez entrer un montant entre 0.01$ et 500.00$", "error")
        except Exception:
            flash("Montant invalide. Veuillez entrer un nombre valide.", "error")
    
    return render_template("balance.html", user=user)

@app.route("/orders")
def orders():
    auth_check = require_login()
    if auth_check: return auth_check
    
    user = get_current_user()
    reservations_query = Reservation.query.filter_by(user_id=user.user_id).order_by(Reservation.reservation_datetime.desc())
    
    selected_month = request.args.get("month")
    selected_month_name = "Toutes les périodes"
    
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
    
    from collections import defaultdict
    monthly_totals = defaultdict(lambda: {"count": 0, "total": Decimal("0.0")})
    for reservation in reservations_query.all():
        month_key = reservation.reservation_datetime.strftime("%Y-%m")
        monthly_totals[month_key]["count"] += 1
        monthly_totals[month_key]["total"] += reservation.total
    
    monthly_summary = {
        month_key: {
            "month_name": datetime(*map(int, month_key.split("-")), 1).strftime("%B %Y"),
            "count": data["count"],
            "total": float(data["total"])
        } for month_key, data in sorted(monthly_totals.items(), reverse=True)
    }
    
    return render_template(
        "orders.html", user=user, orders=reservations, selected_month=selected_month,
        selected_month_name=selected_month_name, monthly_summary=monthly_summary
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

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while creating the menu: {e}", "error")

    return redirect(url_for('admin_dashboard'))


# --- Health Check Route ---

@app.route("/health")
def health_check():
    """Health check endpoint for Docker"""
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 503

# --- Error Handlers ---

def handle_error(error, code):
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

# --- Register Blueprints ---
app.register_blueprint(user_bp)
app.register_blueprint(dish_bp)
app.register_blueprint(cafeteria_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(daily_menu_bp)
app.register_blueprint(daily_menu_item_bp)
app.register_blueprint(order_item_bp)