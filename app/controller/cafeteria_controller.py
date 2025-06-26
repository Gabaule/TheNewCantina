from flask import Blueprint, request, jsonify, session
from functools import wraps
from models.cafeteria import Cafeteria
from models.app_user import AppUser
from models import db

cafeteria_bp = Blueprint('cafeteria_bp', __name__, url_prefix='/api/v1/cafeteria')

# --- Décorateur admin ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Authentification requise"}), 401
        user = AppUser.get_by_id(user_id)
        if not user or user.role != "admin":
            return jsonify({"error": "Accès réservé aux administrateurs"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

# GET /api/v1/cafeteria - Liste toutes les cafétérias (public)
@cafeteria_bp.route('/', methods=['GET'])
def get_all_cafeterias():
    return jsonify(Cafeteria.get_all_dicts()), 200

# GET /api/v1/cafeteria/<int:cafeteria_id> - Affiche une cafétéria (public)
@cafeteria_bp.route('/<int:cafeteria_id>', methods=['GET'])
def get_cafeteria(cafeteria_id):
    cafeteria = Cafeteria.get_by_id(cafeteria_id)
    if not cafeteria:
        return jsonify({'error': 'Cafétéria non trouvée'}), 404
    return jsonify(cafeteria.to_dict()), 200

# POST /api/v1/cafeteria - Créer une cafétéria (ADMIN)
@cafeteria_bp.route('/', methods=['POST'])
@admin_required
def create_cafeteria():
    data = request.get_json()
    try:
        cafeteria = Cafeteria.create_cafeteria(
            name=data['name'],
            address=data.get('address'),
            phone=data.get('phone')
        )
        if cafeteria:
            return jsonify(cafeteria.to_dict()), 201
        else:
            return jsonify({'error': 'Erreur lors de la création (nom en doublon ?)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création', 'details': str(e)}), 400

# PUT /api/v1/cafeteria/<int:cafeteria_id> - Modifier une cafétéria (ADMIN)
@cafeteria_bp.route('/<int:cafeteria_id>', methods=['PUT'])
@admin_required
def update_cafeteria(cafeteria_id):
    cafeteria = Cafeteria.get_by_id(cafeteria_id)
    if not cafeteria:
        return jsonify({'error': 'Cafétéria non trouvée'}), 404
    data = request.get_json()
    success = cafeteria.update_cafeteria(
        name=data.get('name'),
        address=data.get('address'),
        phone=data.get('phone')
    )
    if success:
        return jsonify(cafeteria.to_dict()), 200
    else:
        return jsonify({'error': 'Échec de la mise à jour'}), 400

# DELETE /api/v1/cafeteria/<int:cafeteria_id> - Supprimer une cafétéria (ADMIN)
@cafeteria_bp.route('/<int:cafeteria_id>', methods=['DELETE'])
@admin_required
def delete_cafeteria(cafeteria_id):
    cafeteria = Cafeteria.get_by_id(cafeteria_id)
    if not cafeteria:
        return jsonify({'error': 'Cafétéria non trouvée'}), 404
    if cafeteria.delete_cafeteria():
        return jsonify({'message': 'Cafétéria supprimée'}), 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500
