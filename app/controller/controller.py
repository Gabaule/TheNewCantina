#!/usr/bin/env python3
"""
Flask controller for The New Cantina application
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db
from models.app_user import AppUser
from models.cafeteria import Cafeteria
from models.dish import Dish
from models.daily_menu import DailyMenu
from models.daily_menu_item import DailyMenuItem
from models.reservation import Reservation
from models.order_item import OrderItem

# Create Flask app with correct template folder path
app = Flask(__name__, template_folder='../templates')

# Authentication helper
def require_login():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return None

def get_current_user():
    user_id = session.get("user_id")
    if user_id:
        return AppUser.get_by_id(int(user_id))
    return None

# Routes
@app.route("/")
def index():
    auth_check = require_login()
    if auth_check:
        return auth_check
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        user = AppUser.get_by_email(email)
        if user and user.verify_password(password):
            session["user_id"] = user.user_id
            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect(url_for("dashboard"))
        
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
                DailyMenuItem.menu_id == daily_menu.menu_id,
                Dish.is_available == True
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
        DailyMenuItem.menu_id == daily_menu.menu_id,
        Dish.is_available == True
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
        return {"status": "unhealthy", "error": str(e)}, 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500