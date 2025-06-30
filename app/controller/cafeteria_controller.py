from flask import Blueprint, request, jsonify, session
from functools import wraps
from app.models.cafeteria import Cafeteria       # Correction ici
from app.models.app_user import AppUser          # Correction ici
from app.models import db                        # Correction ici
from app.controller.auth import admin_required, api_require_login   # Correction ici
from sqlalchemy.exc import IntegrityError


cafeteria_bp = Blueprint('cafeteria_bp', __name__, url_prefix='/api/v1/cafeteria')


# --- ROUTES ---

# GET /api/v1/cafeteria - Liste toutes les cafétérias (public)
@cafeteria_bp.route('/', methods=['GET'])
@api_require_login
def get_all_cafeterias(current_user):
    return jsonify(Cafeteria.get_all_dicts()), 200

# GET /api/v1/cafeteria/<int:cafeteria_id> - Affiche une cafétéria (public)
@cafeteria_bp.route('/<int:cafeteria_id>', methods=['GET'])
@api_require_login
def get_cafeteria(cafeteria_id,current_user):
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
            name=data['name']
        )
        db.session.commit()
        return jsonify(cafeteria.to_dict()), 201
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
        name=data.get('name')
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
    try:
        cafeteria.delete_cafeteria()
        # Return an empty response with 200 OK for HTMX.
        return '', 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Suppression impossible. La cafétéria est probablement référencée par un menu ou une commande.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'La suppression a échoué en raison d\'une erreur interne'}), 500