#!/usr/bin/env python3
"""
Flask Main Controller for The New Cantina application
Handles Web Page routes, authentication, and blueprint registration.
"""
import os
import sys
from datetime import datetime
from decimal import Decimal
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


# --- Core Page Routes ---

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

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
            flash(f"Bienvenue, {user.first_name} !", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Identifiants invalides. Veuillez réessayer.", "error")
            return render_template("login.html")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    user = get_current_user()
    user_name = f"{user.first_name} {user.last_name}" if user else "Utilisateur"
    session.clear()
    flash(f"Au revoir, {user_name} ! Vous avez été déconnecté.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@app.route("/dashboard/<int:cafeteria_id>")
def dashboard(cafeteria_id=None):
    # La fonction require_login est maintenant importée de auth.py
    auth_check = require_login() 
    if auth_check: return auth_check
    
    user = get_current_user()
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
                flash(f"Montant de ${amount:.2f} ajouté à votre solde avec succès !", "success")
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