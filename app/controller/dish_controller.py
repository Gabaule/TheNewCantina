from flask import Blueprint, request, jsonify
from models.dish import Dish
from models import db

dish_bp = Blueprint('dish_bp', __name__, url_prefix='/api/v1/dish')

# GET /api/v1/dish - list all dishes
@dish_bp.route('/', methods=['GET'])
def get_all_dishes():
    return jsonify([dish.to_dict() for dish in Dish.query.all()]), 200

# GET /api/v1/dish/<int:dish_id> - get dish by id
@dish_bp.route('/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    return jsonify(dish.to_dict()), 200

# POST /api/v1/dish - create new dish
@dish_bp.route('/', methods=['POST'])
def create_dish():
    data = request.get_json()
    try:
        dish = Dish.create_dish(
            name=data['name'],
            description=data.get('description'),
            dine_in_price=float(data['dine_in_price']),
            is_available=data.get('is_available', True),
            dish_type=data['dish_type']
        )
        if dish:
            return jsonify(dish.to_dict()), 201
        else:
            return jsonify({'error': 'Dish creation failed (possibly duplicate name or constraint error).'}), 400
    except (KeyError, TypeError, ValueError):
        return jsonify({'error': 'Invalid data provided'}), 400

# PUT /api/v1/dish/<int:dish_id> - update dish
@dish_bp.route('/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    data = request.get_json()
    updated = dish.update_dish(
        name=data.get('name'),
        description=data.get('description'),
        dine_in_price=float(data['dine_in_price']) if data.get('dine_in_price') is not None else None,
        is_available=data.get('is_available'),
        dish_type=data.get('dish_type')
    )
    if updated:
        return jsonify(dish.to_dict()), 200
    else:
        return jsonify({'error': 'Update failed'}), 400

# DELETE /api/v1/dish/<int:dish_id> - delete dish
@dish_bp.route('/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    if dish.delete_dish():
        return jsonify({'message': 'Dish deleted'}), 200
    else:
        return jsonify({'error': 'Deletion failed'}), 500
