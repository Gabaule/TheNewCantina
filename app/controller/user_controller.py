# app/controller/user_controller.py

from flask import Blueprint, request, jsonify, session
from models.app_user import AppUser
from models import db
from controller import admin_required

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/user')


# GET /api/v1/user - Liste tous les utilisateurs (admin seulement)
@user_bp.route('/', methods=['GET'])
def list_users():
    # Protection basique (améliorable)
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({'error': 'Authentification requise'}), 401
    user = AppUser.get_by_id(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Accès interdit'}), 403
    return jsonify(AppUser.get_all_dicts()), 200


# GET /api/v1/user/<int:user_id> - Récupérer un utilisateur par ID (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    requester_id = session.get("user_id")
    if not requester_id:
        return jsonify({'error': 'Authentification requise'}), 401
    user = AppUser.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    # Autorisé si admin ou soi-même
    requester = AppUser.get_by_id(requester_id)
    if requester.role != 'admin' and requester.user_id != user.user_id:
        return jsonify({'error': 'Accès interdit'}), 403
    return jsonify(user.to_dict()), 200


# POST /api/v1/user - Création d’un utilisateur
@user_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    try:
        user = AppUser.create_user(
            last_name=data['last_name'],
            first_name=data['first_name'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'student'),
            balance=float(data.get('balance', 0.0))
        )
        if user:
            return jsonify(user.to_dict()), 201
        else:
            return jsonify({'error': 'Email déjà utilisé'}), 409
    except (KeyError, TypeError, ValueError):
        return jsonify({'error': 'Données invalides'}), 400


# PUT /api/v1/user/<int:user_id> - Modifier un utilisateur (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    requester_id = session.get("user_id")
    if not requester_id:
        return jsonify({'error': 'Authentification requise'}), 401
    requester = AppUser.get_by_id(requester_id)
    if not requester:
        return jsonify({'error': 'Utilisateur inconnu'}), 404
    if requester.role != 'admin' and requester.user_id != user_id:
        return jsonify({'error': 'Accès interdit'}), 403
    user = AppUser.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    data = request.get_json()
    success = user.update_user(
        last_name=data.get('last_name'),
        first_name=data.get('first_name'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role'),
        balance=float(data['balance']) if data.get('balance') is not None else None
    )
    if success:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'Échec de la mise à jour'}), 400


# DELETE /api/v1/user/<int:user_id> - Supprimer un utilisateur (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    requester_id = session.get("user_id")
    if not requester_id:
        return jsonify({'error': 'Authentification requise'}), 401
    requester = AppUser.get_by_id(requester_id)
    if not requester:
        return jsonify({'error': 'Utilisateur inconnu'}), 404
    if requester.role != 'admin' and requester.user_id != user_id:
        return jsonify({'error': 'Accès interdit'}), 403
    user = AppUser.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    if user.delete_user():
        return jsonify({'message': 'Utilisateur supprimé'}), 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500

