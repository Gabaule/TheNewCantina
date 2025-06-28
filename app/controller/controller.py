#!/usr/bin/env python3
"""
Flask Main Controller for The New Cantina application
Handles Web Page routes, authentication, and blueprint registration.
"""
import os
import sys
from datetime import datetime, date
from decimal import Decimal
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from sqlalchemy import text
import json

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

# Add tojson filter to Jinja environment
app.jinja_env.filters['tojson'] = lambda obj: json.dumps(obj)

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
    """
    Renders the advanced menu creation form.
    Provides all cafeterias and dishes for the dynamic interface.
    """
    selected_date_str = request.args.get("date", date.today().strftime('%Y-%m-%d'))

    all_cafeterias = Cafeteria.query.order_by(Cafeteria.name).all()
    all_dishes_list = Dish.query.order_by(Dish.name).all()
    
    # Group dishes by type for the JavaScript (for autocomplete functionality)
    grouped_dishes = {
        'main_course': [], 'soup': [], 'side_dish': [], 'drink': []
    }
    for dish in all_dishes_list:
        if dish.dish_type in grouped_dishes:
            grouped_dishes[dish.dish_type].append({
                'dish_id': dish.dish_id,
                'name': dish.name,
                'description': dish.description,
                'dine_in_price': float(dish.dine_in_price),
                'dish_type': dish.dish_type
            })

    return render_template(
        "admin/dashboard.html",
        user=current_user,
        cafeterias=all_cafeterias,
        dishes=grouped_dishes,  # This will be converted to JSON in the template
        selected_date=selected_date_str
    )

@app.route("/admin/menu", methods=['POST'])
@admin_web_required
def create_admin_menu(current_user):
    """
    Handles the submission from the advanced menu creation form.
    Creates dishes and assigns them to multiple cafeterias for the given date.
    """
    menu_date_str = request.form.get('menu_date')
    
    try:
        if not menu_date_str:
            flash("Menu date is required.", "error")
            return redirect(url_for('admin_dashboard'))

        menu_date = datetime.strptime(menu_date_str, "%Y-%m-%d").date()
        
        # Parse dishes from the form
        dishes_data = []
        dish_index = 0
        
        while f'dishes[{dish_index}][name]' in request.form:
            dish_name = request.form.get(f'dishes[{dish_index}][name]', '').strip()
            dish_description = request.form.get(f'dishes[{dish_index}][description]', '').strip()
            dish_price = request.form.get(f'dishes[{dish_index}][dine_in_price]')
            dish_type = request.form.get(f'dishes[{dish_index}][dish_type]')
            selected_cafeterias = request.form.getlist(f'dishes[{dish_index}][cafeterias]')
            
            if dish_name and dish_price and dish_type and selected_cafeterias:
                try:
                    price = float(dish_price)
                    cafeteria_ids = [int(cid) for cid in selected_cafeterias]
                    
                    dishes_data.append({
                        'name': dish_name,
                        'description': dish_description,
                        'dine_in_price': price,
                        'dish_type': dish_type,
                        'cafeteria_ids': cafeteria_ids
                    })
                except (ValueError, TypeError):
                    flash(f"Invalid price or cafeteria selection for dish '{dish_name}'", "error")
                    return redirect(url_for('admin_dashboard', date=menu_date_str))
            
            dish_index += 1
        
        if not dishes_data:
            flash("At least one dish with valid data and cafeteria selection is required.", "error")
            return redirect(url_for('admin_dashboard', date=menu_date_str))

        # Track which cafeterias we're updating
        affected_cafeterias = set()
        for dish_data in dishes_data:
            affected_cafeterias.update(dish_data['cafeteria_ids'])

        # Clear existing menus for the selected date and cafeterias
        for cafeteria_id in affected_cafeterias:
            existing_menu = DailyMenu.query.filter_by(
                cafeteria_id=cafeteria_id, menu_date=menu_date
            ).first()
            if existing_menu:
                # Clear existing items
                DailyMenuItem.query.filter_by(menu_id=existing_menu.menu_id).delete()

        # Process each dish
        created_dishes = []
        for dish_data in dishes_data:
            # Check if dish already exists by name (exact match)
            existing_dish = Dish.query.filter_by(name=dish_data['name']).first()
            
            if existing_dish:
                # Update existing dish with new data
                existing_dish.description = dish_data['description']
                existing_dish.dine_in_price = dish_data['dine_in_price']
                existing_dish.dish_type = dish_data['dish_type']
                dish = existing_dish
            else:
                # Create new dish
                dish = Dish(
                    name=dish_data['name'],
                    description=dish_data['description'],
                    dine_in_price=dish_data['dine_in_price'],
                    dish_type=dish_data['dish_type']
                )
                db.session.add(dish)
                db.session.flush()  # Get the dish_id
            
            created_dishes.append((dish, dish_data['cafeteria_ids']))

        # Create/update daily menus and add items
        display_order = 1
        for dish, cafeteria_ids in created_dishes:
            for cafeteria_id in cafeteria_ids:
                # Get or create daily menu for this cafeteria and date
                daily_menu = DailyMenu.query.filter_by(
                    cafeteria_id=cafeteria_id, menu_date=menu_date
                ).first()
                
                if not daily_menu:
                    daily_menu = DailyMenu(
                        cafeteria_id=cafeteria_id,
                        menu_date=menu_date
                    )
                    db.session.add(daily_menu)
                    db.session.flush()  # Get the menu_id

                # Add dish to this menu
                menu_item = DailyMenuItem(
                    menu_id=daily_menu.menu_id,
                    dish_id=dish.dish_id,
                    dish_role=dish.dish_type,
                    display_order=display_order
                )
                db.session.add(menu_item)
            
            display_order += 1

        db.session.commit()
        
        cafeteria_names = [c.name for c in Cafeteria.query.filter(Cafeteria.cafeteria_id.in_(affected_cafeterias)).all()]
        flash(f"Menu for {menu_date_str} created/updated successfully for {', '.join(cafeteria_names)}! Added {len(created_dishes)} dishes.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
        import traceback
        traceback.print_exc()

    return redirect(url_for('admin_dashboard', date=menu_date_str or ''))


@app.route("/admin/users")
@admin_web_required
def admin_users(current_user):
    all_users = AppUser.query.order_by(AppUser.last_name, AppUser.first_name).all()
    return render_template("admin/users.html", user=current_user, users=all_users)


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