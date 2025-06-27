from flask import Blueprint, request, jsonify, session
from functools import wraps
from models.dish import Dish
from models.app_user import AppUser
from models import db
from .auth import admin_required, api_require_login

dish_bp = Blueprint('dish_bp', __name__, url_prefix='/api/v1/dish')

# --- ROUTES ---

# GET /api/v1/dish - Liste tous les plats (lecture publique)
@dish_bp.route('/', methods=['GET'])
def get_all_dishes():
    return jsonify([dish.to_dict() for dish in Dish.query.all()]), 200

# GET /api/v1/dish/<int:dish_id> - Affiche un plat (lecture publique)
@dish_bp.route('/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Plat non trouvé'}), 404
    return jsonify(dish.to_dict()), 200

# POST /api/v1/dish - Créer un plat (ADMIN)
@dish_bp.route('/', methods=['POST'])
@admin_required
def create_dish():
    data = request.get_json()
    try:
        dish = Dish(
            name=data['name'],
            description=data.get('description'),
            dine_in_price=float(data['dine_in_price']),
            dish_type=data['dish_type']
        )
        db.session.add(dish)
        db.session.commit()
        return jsonify(dish.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création du plat', 'details': str(e)}), 400

# PUT /api/v1/dish/<int:dish_id> - Modifier un plat (ADMIN)
@dish_bp.route('/<int:dish_id>', methods=['PUT'])
@admin_required
def update_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Plat non trouvé'}), 404
    data = request.get_json()
    try:
        for field in ['name', 'description', 'dine_in_price', 'dish_type']:
            if field in data:
                setattr(dish, field, data[field])
        db.session.commit()
        return jsonify(dish.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour', 'details': str(e)}), 400

# DELETE /api/v1/dish/<int:dish_id> - Supprimer un plat (ADMIN)
@dish_bp.route('/<int:dish_id>', methods=['DELETE'])
@admin_required
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Plat non trouvé'}), 404
    try:
        db.session.delete(dish)
        db.session.commit()
        return jsonify({'message': 'Plat supprimé'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la suppression', 'details': str(e)}), 500
