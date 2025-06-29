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
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, make_response
from sqlalchemy import text
from sqlalchemy.orm import joinedload
import json
from collections import defaultdict
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Model imports
from models import db, AppUser, Cafeteria, Dish, DailyMenu, DailyMenuItem, Reservation, OrderItem

# --- Util/Auth Helper Imports ---
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
app.jinja_env.filters['tojson'] = lambda obj: json.dumps(obj)

# --- Authentication & Authorization Helpers ---
def admin_web_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if auth_check := require_login(): return auth_check
        user = get_current_user()
        if not user or user.role != "admin":
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for("dashboard"))
        return f(current_user=user, *args, **kwargs)
    return decorated_function

# --- Core Page Routes ---
@app.route("/")
def index():
    if "user_id" in session:
        user = get_current_user()
        return redirect(url_for("admin_dashboard") if user and user.role == 'admin' else url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session: return redirect(url_for("index"))
    if request.method == "POST":
        user = AppUser.get_by_email(request.form.get("username"))
        if user and user.verify_password(request.form.get("password")):
            session["user_id"], session.permanent = user.user_id, True
            session.pop('cart', None)
            return redirect(url_for("admin_dashboard") if user.role == 'admin' else url_for("dashboard"))
        flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Cart & Dashboard ---
def get_cart_details():
    cart_session = session.get('cart', {})
    if not cart_session: return [], Decimal('0.0')
    dish_ids = [int(k) for k in cart_session.keys()]
    dishes = Dish.query.filter(Dish.dish_id.in_(dish_ids)).all()
    dish_map = {str(d.dish_id): d for d in dishes}
    items, total = [], Decimal('0.0')
    for dish_id_str, data in cart_session.items():
        if dish := dish_map.get(dish_id_str):
            quantity = data.get('quantity', 1)
            subtotal = dish.dine_in_price * quantity
            total += subtotal
            items.append({'dish': dish, 'quantity': quantity, 'subtotal': subtotal})
    return items, total

@app.route("/dashboard")
@app.route("/dashboard/<int:cafeteria_id>")
def dashboard(cafeteria_id=None):
    if auth_check := require_login(): return auth_check
    user = get_current_user()
    if user.role == 'admin': return redirect(url_for('admin_dashboard'))
    
    if not cafeteria_id:
        if first_caf := Cafeteria.query.first():
            return redirect(url_for("dashboard", cafeteria_id=first_caf.cafeteria_id))
        flash("No cafeterias are configured in the system.", "warning")
        return render_template("layout.html", user=user, current_cafeteria=None, cafeterias=[], selected_date=date.today().strftime("%Y-%m-%d"))

    session['current_cafeteria_id'] = cafeteria_id
    current_cafeteria = Cafeteria.query.get_or_404(cafeteria_id)
    selected_date_str = request.args.get("date", date.today().strftime("%Y-%m-%d"))
    selected_date_obj = datetime.strptime(selected_date_str, "%Y-%m-%d").date()

    menu_items = []
    if daily_menu := DailyMenu.query.filter_by(cafeteria_id=cafeteria_id, menu_date=selected_date_obj).first():
        menu_items = db.session.query(Dish, DailyMenuItem).join(DailyMenuItem).filter(DailyMenuItem.menu_id == daily_menu.menu_id).order_by(DailyMenuItem.display_order).all()

    cart_items, cart_total = get_cart_details()
    
    return render_template("dashboard.html", user=user, cafeterias=Cafeteria.query.all(),
        current_cafeteria=current_cafeteria, selected_date=selected_date_str,
        menu=menu_items, cart_items=cart_items, cart_total=cart_total)

@app.route('/cart/action/<string:action>/<int:dish_id>', methods=['POST'])
def handle_cart_action(action, dish_id):
    if auth_check := require_login(): return auth_check
    cart = session.get('cart', {})
    dish_id_str = str(dish_id)
    if action == 'add' and Dish.get_by_id(dish_id):
        cart[dish_id_str] = {'quantity': 1}
    elif action == 'update' and dish_id_str in cart:
        quantity = int(request.form.get('quantity', 1))
        if quantity > 0: cart[dish_id_str]['quantity'] = quantity
        else: del cart[dish_id_str]
    elif action == 'remove' and dish_id_str in cart:
        del cart[dish_id_str]
    session['cart'] = cart
    return redirect(url_for('dashboard', cafeteria_id=session.get('current_cafeteria_id')))

@app.route("/order", methods=['POST'])
def place_order():
    if auth_check := require_login(): return auth_check
    user = get_current_user()
    cart_items, total_cost = get_cart_details()
    cafeteria_id = session.get('current_cafeteria_id')

    if not all([cart_items, cafeteria_id, user.balance >= total_cost]):
        flash("Order failed: Check cart, cafeteria selection, or your balance.", "error")
        return redirect(url_for('dashboard', cafeteria_id=cafeteria_id))
    try:
        reservation = Reservation(user_id=user.user_id, cafeteria_id=cafeteria_id, total=total_cost, status='completed')
        db.session.add(reservation)
        db.session.flush()
        for item in cart_items:
            order_item = OrderItem(reservation_id=reservation.reservation_id, dish_id=item['dish'].dish_id, quantity=item['quantity'], applied_price=item['dish'].dine_in_price, is_takeaway=False)
            db.session.add(order_item)
        user.balance -= total_cost
        db.session.commit()
        session.pop('cart', None)
        flash("Order placed successfully!", "success")
        response = make_response()
        response.headers['HX-Redirect'] = url_for('orders')
        return response
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred during checkout: {e}", "error")
        return redirect(url_for('dashboard', cafeteria_id=cafeteria_id))

# --- Account Pages ---
@app.route("/balance", methods=["GET", "POST"])
def balance():
    if auth_check := require_login(): return auth_check
    user = get_current_user()

    # Provide context for layout.html
    cafeteria_id = session.get('current_cafeteria_id')
    current_cafeteria = Cafeteria.query.get(cafeteria_id) if cafeteria_id else Cafeteria.query.first()
    cafeterias = Cafeteria.query.all()
    selected_date = date.today().strftime("%Y-%m-%d")

    context = {
        "user": user,
        "current_cafeteria": current_cafeteria,
        "cafeterias": cafeterias,
        "selected_date": selected_date
    }

    if request.method == "POST":
        try:
            amount = Decimal(request.form.get("amount", "0"))
            if Decimal("0.01") <= amount <= Decimal("500.00"):
                user.balance += amount
                db.session.commit()
                context.update({"success_msg": f"${amount:.2f} was added.", "user": get_current_user()})
            else: context["error_msg"] = "Amount must be between $0.01 and $500.00."
        except Exception: context["error_msg"] = "Invalid amount provided."
    return render_template("balance.html", **context)

@app.route("/orders")
def orders():
    if auth_check := require_login(): return auth_check
    user = get_current_user()

    # Provide context for layout.html to prevent crashing
    cafeteria_id = session.get('current_cafeteria_id')
    current_cafeteria = Cafeteria.query.get(cafeteria_id) if cafeteria_id else Cafeteria.query.first()
    cafeterias = Cafeteria.query.all()
    selected_date = date.today().strftime("%Y-%m-%d")
    
    query = Reservation.query.filter_by(user_id=user.user_id).order_by(Reservation.reservation_datetime.desc())
    
    selected_month = request.args.get("month")
    selected_month_name = "All Periods"
    
    if selected_month:
        try:
            year, month = map(int, selected_month.split("-"))
            reservations = query.filter(db.extract('year', Reservation.reservation_datetime) == year, db.extract('month', Reservation.reservation_datetime) == month).all()
            selected_month_name = datetime(year, month, 1).strftime("%B %Y")
        except (ValueError, IndexError):
            selected_month = None
            reservations = query.all()
    else:
        reservations = query.all()

    context = {
        "user": user, 
        "orders": reservations, 
        "selected_month": selected_month, 
        "selected_month_name": selected_month_name,
        "current_cafeteria": current_cafeteria,
        "cafeterias": cafeterias,
        "selected_date": selected_date
    }
    
    # Calculate summary only for full page loads to populate the sidebar
    if 'HX-Request' not in request.headers:
        monthly_totals = defaultdict(lambda: {"count": 0, "total": Decimal("0.0")})
        all_user_orders = Reservation.query.filter_by(user_id=user.user_id).all()
        for r in all_user_orders:
            month_key = r.reservation_datetime.strftime("%Y-%m")
            monthly_totals[month_key]["count"] += 1
            monthly_totals[month_key]["total"] += r.total
        context["monthly_summary"] = {k: {"month_name": datetime.strptime(k, "%Y-%m").strftime("%B %Y"), **v} for k, v in sorted(monthly_totals.items(), reverse=True)}

    return render_template("orders.html", **context)

# --- Admin Routes ---
@app.route("/admin/dashboard")
@admin_web_required
def admin_dashboard(current_user):
    selected_date_str = request.args.get("date", date.today().strftime('%Y-%m-%d'))
    try:
        selected_date_obj = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date_str = date.today().strftime('%Y-%m-%d')
        selected_date_obj = date.today()
        flash("Invalid date format, defaulting to today.", "warning")

    all_cafeterias = Cafeteria.query.order_by(Cafeteria.name).all()
    all_dishes = Dish.query.order_by(Dish.name).all()

    # Build a dictionary of dishes on the menu for the selected date
    dishes_on_menu = defaultdict(lambda: {'dish': None, 'cafeteria_ids': set()})
    
    # Eager load related dishes to avoid N+1 queries in the loop
    menu_items_for_date = db.session.query(DailyMenuItem, DailyMenu.cafeteria_id).\
        join(DailyMenu, DailyMenuItem.menu_id == DailyMenu.menu_id).\
        filter(DailyMenu.menu_date == selected_date_obj).\
        options(joinedload(DailyMenuItem.dish)).\
        all()

    for menu_item, cafeteria_id in menu_items_for_date:
        dish = menu_item.dish
        if dish:
            dishes_on_menu[dish.dish_id]['dish'] = dish
            dishes_on_menu[dish.dish_id]['cafeteria_ids'].add(cafeteria_id)

    # Convert the defaultdict to a list of dicts for the template
    menu_for_template = []
    for dish_id, data in sorted(dishes_on_menu.items()):
        dish_dict = data['dish'].to_dict()
        dish_dict['cafeteria_ids'] = sorted(list(data['cafeteria_ids']))
        menu_for_template.append(dish_dict)
    
    menu_for_template.sort(key=lambda x: x['name'])

    return render_template("admin/dashboard.html",
                           user=current_user,
                           all_cafeterias=[c.to_dict() for c in all_cafeterias],
                           all_dishes=[d.to_dict() for d in all_dishes],
                           dishes_on_menu=menu_for_template,
                           selected_date=selected_date_str)

@app.route("/admin/menu", methods=['POST'])
@admin_web_required
def create_admin_menu(current_user):
    menu_date_str = request.form.get('menu_date')
    try:
        menu_date = datetime.strptime(menu_date_str, "%Y-%m-%d").date()

        # Delete all menu items and menus for this date to ensure a clean slate.
        # Cascade will handle deleting items.
        DailyMenu.query.filter_by(menu_date=menu_date).delete()
        db.session.flush()

        # Process submitted dishes
        dishes_to_process = []
        i = 0
        while f"dishes[{i}][name]" in request.form:
            name = request.form.get(f"dishes[{i}][name]", "").strip()
            if name: # Only process rows that have a dish name
                cafeteria_ids = [int(cid) for cid in request.form.getlist(f"dishes[{i}][cafeterias]")]
                if not cafeteria_ids: # Skip if no cafeterias are selected
                    i += 1
                    continue
                
                dishes_to_process.append({
                    "dish_id": request.form.get(f"dishes[{i}][dish_id]"),
                    "name": name,
                    "description": request.form.get(f"dishes[{i}][description]", "").strip(),
                    "dine_in_price": Decimal(request.form.get(f"dishes[{i}][dine_in_price]", "0.0")),
                    "dish_type": request.form.get(f"dishes[{i}][dish_type]"),
                    "cafeteria_ids": cafeteria_ids,
                })
            i += 1
        
        menu_cache = {} # Cache for DailyMenu instances {cafeteria_id: menu_object}

        for dish_data in dishes_to_process:
            dish = None
            # If an ID is provided and the name hasn't changed, use that dish.
            if dish_data['dish_id'] and dish_data['dish_id'].isdigit():
                temp_dish = Dish.get_by_id(int(dish_data['dish_id']))
                if temp_dish and temp_dish.name == dish_data['name']:
                    dish = temp_dish

            # If no dish was found by ID (or name was changed), find by name.
            if not dish:
                dish = Dish.query.filter(Dish.name.ilike(dish_data['name'])).first()
            
            if dish: # Update existing dish
                dish.description = dish_data['description']
                dish.dine_in_price = dish_data['dine_in_price']
                dish.dish_type = dish_data['dish_type']
            else: # Create new dish
                dish = Dish(
                    name=dish_data['name'],
                    description=dish_data['description'],
                    dine_in_price=dish_data['dine_in_price'],
                    dish_type=dish_data['dish_type']
                )
            db.session.add(dish)
            db.session.flush() # Ensure dish has an ID

            for cid in dish_data['cafeteria_ids']:
                menu = menu_cache.get(cid)
                if not menu:
                    menu = DailyMenu(cafeteria_id=cid, menu_date=menu_date)
                    db.session.add(menu)
                    db.session.flush()
                    menu_cache[cid] = menu
                
                item = DailyMenuItem(menu_id=menu.menu_id, dish_id=dish.dish_id, dish_role=dish_data['dish_type'])
                db.session.add(item)
        
        db.session.commit()
        flash(f"Menus for {menu_date_str} updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
        traceback.print_exc()
    return redirect(url_for('admin_dashboard', date=menu_date_str or ''))


@app.route("/admin/users")
@admin_web_required
def admin_users(current_user):
    return render_template("admin/users.html", user=current_user, users=AppUser.query.order_by(AppUser.last_name, AppUser.first_name).all())

# --- Health & Error Handling ---
@app.route("/health")
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 503

@app.errorhandler(404)
def not_found(error): return render_template("404.html", error=error), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    traceback.print_exc()
    return render_template("500.html", error=error), 500

# --- Blueprints ---
app.register_blueprint(user_bp)
app.register_blueprint(dish_bp)
app.register_blueprint(cafeteria_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(daily_menu_bp)
app.register_blueprint(daily_menu_item_bp)
app.register_blueprint(order_item_bp)