# app/controller/user_controller.py

from flask import Blueprint, request, jsonify, session
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

# IMPORTS ABSOLUS OBLIGATOIRES :
from app.models.app_user import AppUser
from app.models import db
from app.controller.auth import admin_required, api_require_login

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/user')


# GET /api/v1/user - Liste tous les utilisateurs (admin seulement)
@user_bp.route('/', methods=['GET'])
@admin_required
def list_users():
    return jsonify(AppUser.get_all_dicts()), 200


# GET /api/v1/user/<int:user_id> - Récupérer un utilisateur par ID (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['GET'])
@api_require_login
def get_user(current_user, user_id):
    user = AppUser.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    # Autorisé si admin ou soi-même
    if current_user.role != 'admin' and current_user.user_id != user.user_id:
        return jsonify({'error': 'Accès interdit'}), 403
    return jsonify(user.to_dict()), 200


# POST /api/v1/user - Création d’un utilisateur (ADMIN)
@user_bp.route('/', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    try:
        if not data or not all(k in data and data[k] for k in ['last_name', 'first_name', 'email', 'password']):
            return jsonify({'error': 'Données manquantes. Les champs nom, prénom, email et mot de passe sont obligatoires.'}), 400

        user = AppUser.create_user(
            last_name=data['last_name'],
            first_name=data['first_name'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'student'),
            balance=float(data.get('balance', 0.0))
        )
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': f"L'email '{data.get('email')}' est déjà utilisé."}), 409
    except (KeyError, TypeError, ValueError):
        db.session.rollback()
        return jsonify({'error': 'Données invalides. Vérifiez les types de données (ex: le solde doit être un nombre).'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Une erreur interne est survenue', 'details': str(e)}), 500


# PUT /api/v1/user/<int:user_id> - Modifier un utilisateur (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['PUT'])
@api_require_login
def update_user(current_user, user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        return jsonify({'error': 'Accès interdit'}), 403
    
    user_to_update = AppUser.get_by_id(user_id)
    if not user_to_update:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
    data = request.get_json()
    # Admins can change roles, others cannot.
    role = data.get('role') if current_user.role == 'admin' else None

    success = user_to_update.update_user(
        last_name=data.get('last_name'),
        first_name=data.get('first_name'),
        email=data.get('email'),
        password=data.get('password'),
        role=role,
        balance=float(data['balance']) if 'balance' in data and current_user.role == 'admin' else None
    )
    if success:
        return jsonify(user_to_update.to_dict()), 200
    else:
        return jsonify({'error': 'Échec de la mise à jour'}), 400


# DELETE /api/v1/user/<int:user_id> - Supprimer un utilisateur (admin ou soi-même)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@api_require_login
def delete_user(current_user, user_id):
    if current_user.role != 'admin' and current_user.user_id != user_id:
        return jsonify({'error': 'Accès interdit'}), 403
        
    user_to_delete = AppUser.get_by_id(user_id)
    if not user_to_delete:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
    if user_to_delete.delete_user():
        if current_user.user_id == user_id: # If user deletes themself
            session.clear()
        # Return an empty response with 200 OK.
        # HTMX will swap the target (the <tr>) with this empty response,
        # effectively deleting the row from the table.
        return '', 200
    else:
        return jsonify({'error': 'Suppression impossible'}), 500

# POST /api/v1/user/balance - Créditer le solde de l'utilisateur connecté
@user_bp.route('/balance', methods=['POST'])
@api_require_login
def add_to_balance(current_user):
    """Add funds to the current user's balance."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corps de la requête invalide."}), 400
    try:
        amount = Decimal(data.get("amount", "0"))
        if Decimal("0.01") <= amount <= Decimal("500.00"):
            current_user.balance += amount
            db.session.commit()
            return jsonify({
                "message": f"Montant de ${amount:.2f} ajouté à votre solde avec succès !",
                "new_balance": float(current_user.balance)
            }), 200
        else:
            return jsonify({"error": "Veuillez entrer un montant entre 0.01$ et 500.00$"}), 400
    except Exception:
        return jsonify({"error": "Montant invalide. Veuillez entrer un nombre valide."}), 400