# app/controller/order_item_controller.py

from flask import Blueprint, request, jsonify
from models import db
from models.order_item import OrderItem
from .auth import admin_required, api_require_login

order_item_bp = Blueprint('order_item_bp', __name__, url_prefix='/api/v1/order-item')

# --- ROUTES (ADMIN-ONLY) ---
# Les OrderItems sont normalement gérés via les réservations.
# Ces routes sont pour l'administration directe.

# GET /api/v1/order-item - Liste tous les items de commande (ADMIN)
@order_item_bp.route('/', methods=['GET'])
@admin_required
def get_all_order_items():
    items = OrderItem.get_all_dicts()
    return jsonify(items), 200

# GET /api/v1/order-item/<int:item_id> - Affiche un item de commande (ADMIN)
@order_item_bp.route('/<int:item_id>', methods=['GET'])
@admin_required
def get_order_item(item_id):
    item = OrderItem.get_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item de commande non trouvé'}), 404
    return jsonify(item.to_dict()), 200

# DELETE /api/v1/order-item/<int:item_id> - Supprime un item de commande (ADMIN)
@order_item_bp.route('/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_order_item(item_id):
    item = OrderItem.get_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item de commande non trouvé'}), 404
    if item.delete_order_item():
        return jsonify({'message': 'Item de commande supprimé'}), 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500