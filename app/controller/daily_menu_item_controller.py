# app/controller/daily_menu_item_controller.py

from flask import Blueprint, request, jsonify
from models import db
from models.daily_menu_item import DailyMenuItem
from .auth import admin_required, api_require_login

daily_menu_item_bp = Blueprint('daily_menu_item_bp', __name__, url_prefix='/api/v1/daily-menu-item')

# --- ROUTES ---

# Note : Les opérations sur les 'daily_menu_item' sont généralement des tâches administratives
# pour construire un menu. L'accès est donc restreint aux admins.

# GET /api/v1/daily-menu-item/by-menu/<int:menu_id> - Lister les items d'un menu
@daily_menu_item_bp.route('/by-menu/<int:menu_id>', methods=['GET'])
@admin_required
def get_items_for_menu(menu_id):
    items = DailyMenuItem.query.filter_by(menu_id=menu_id).all()
    return jsonify([item.to_dict() for item in items]), 200

# POST /api/v1/daily-menu-item - Ajouter un plat à un menu (ADMIN)
@daily_menu_item_bp.route('/', methods=['POST'])
@admin_required
def create_menu_item():
    data = request.get_json()
    try:
        item = DailyMenuItem.create_menu_item(
            menu_id=data['menu_id'],
            dish_id=data['dish_id'],
            dish_role=data['dish_role'],
            display_order=data.get('display_order', 1)
        )
        db.session.commit()
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création de l\'item de menu', 'details': str(e)}), 400

# PUT /api/v1/daily-menu-item/<int:item_id> - Modifier un item de menu (ADMIN)
@daily_menu_item_bp.route('/<int:item_id>', methods=['PUT'])
@admin_required
def update_menu_item(item_id):
    item = DailyMenuItem.get_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item de menu non trouvé'}), 404
    data = request.get_json()
    success = item.update_menu_item(
        dish_id=data.get('dish_id'),
        dish_role=data.get('dish_role'),
        display_order=data.get('display_order')
    )
    if success:
        return jsonify(item.to_dict()), 200
    else:
        return jsonify({'error': 'Échec de la mise à jour'}), 400

# DELETE /api/v1/daily-menu-item/<int:item_id> - Supprimer un item d'un menu (ADMIN)
@daily_menu_item_bp.route('/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_menu_item(item_id):
    item = DailyMenuItem.get_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item de menu non trouvé'}), 404
    if item.delete_menu_item():
        return jsonify({'message': 'Item de menu supprimé'}), 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500