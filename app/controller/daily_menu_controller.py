# app/controller/daily_menu_controller.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db
from models.daily_menu import DailyMenu
from models.dish import Dish
from models.daily_menu_item import DailyMenuItem
from .auth import admin_required, api_require_login

daily_menu_bp = Blueprint('daily_menu_bp', __name__, url_prefix='/api/v1/daily-menu')

# --- ROUTES ---

# GET /api/v1/daily-menu/ - Liste tous les menus (ADMIN)
@daily_menu_bp.route('/', methods=['GET'])
@admin_required
def get_all_menus():
    menus = DailyMenu.get_all_dicts()
    return jsonify(menus), 200

# GET /api/v1/daily-menu/<int:menu_id> - Affiche un menu (ADMIN)
@daily_menu_bp.route('/<int:menu_id>', methods=['GET'])
@admin_required
def get_menu(menu_id):
    menu = DailyMenu.get_by_id(menu_id)
    if not menu:
        return jsonify({'error': 'Menu non trouvé'}), 404
    return jsonify(menu.to_dict()), 200

# GET /api/v1/daily-menu/by-cafeteria/<int:cafeteria_id> - Récupère le menu d'une cafétéria pour une date donnée (AUTHENTIFIÉ)
@daily_menu_bp.route('/by-cafeteria/<int:cafeteria_id>', methods=['GET'])
@api_require_login
def get_menu_for_cafeteria(current_user, cafeteria_id):
    selected_date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Format de date invalide. Utilisez YYYY-MM-DD."}), 400

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
            "dish_id": dish.dish_id, "name": dish.name, "description": dish.description,
            "price": float(dish.dine_in_price), "dish_type": dish.dish_type, "role": menu_item.dish_role
        } for dish, menu_item in menu_items
    ]
    return jsonify({"menu": menu_data}), 200


# POST /api/v1/daily-menu - Créer un menu (ADMIN)
@daily_menu_bp.route('/', methods=['POST'])
@admin_required
def create_menu():
    data = request.get_json()
    try:
        menu_date = datetime.strptime(data['menu_date'], '%Y-%m-%d').date()
        menu = DailyMenu.create_menu(
            cafeteria_id=data['cafeteria_id'],
            menu_date=menu_date
        )
        db.session.commit()
        return jsonify(menu.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création du menu', 'details': str(e)}), 400

# PUT /api/v1/daily-menu/<int:menu_id> - Modifier un menu (ADMIN)
@daily_menu_bp.route('/<int:menu_id>', methods=['PUT'])
@admin_required
def update_menu(menu_id):
    menu = DailyMenu.get_by_id(menu_id)
    if not menu:
        return jsonify({'error': 'Menu non trouvé'}), 404
    data = request.get_json()
    menu_date = datetime.strptime(data['menu_date'], '%Y-%m-%d').date() if data.get('menu_date') else None
    
    success = menu.update_menu(
        cafeteria_id=data.get('cafeteria_id'),
        menu_date=menu_date
    )
    if success:
        return jsonify(menu.to_dict()), 200
    else:
        return jsonify({'error': 'Échec de la mise à jour'}), 400

# DELETE /api/v1/daily-menu/<int:menu_id> - Supprimer un menu (ADMIN)
@daily_menu_bp.route('/<int:menu_id>', methods=['DELETE'])
@admin_required
def delete_menu(menu_id):
    menu = DailyMenu.get_by_id(menu_id)
    if not menu:
        return jsonify({'error': 'Menu non trouvé'}), 404
    if menu.delete_menu():
        return jsonify({'message': 'Menu supprimé'}), 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500