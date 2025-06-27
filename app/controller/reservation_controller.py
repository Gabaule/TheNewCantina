# app/controller/reservation_controller.py

from flask import Blueprint, request, jsonify
from decimal import Decimal

# Import necessary models and the db session
from models import db
from models.app_user import AppUser
from models.cafeteria import Cafeteria
from models.dish import Dish
from models.reservation import Reservation
from models.order_item import OrderItem

# Import the authentication decorator from the main controller
from .auth import admin_required, api_require_login

# Create a Blueprint for reservation routes
reservation_bp = Blueprint('reservation_bp', __name__, url_prefix='/api/v1/reservations')

# --- Reservation API Routes ---

@reservation_bp.route('/', methods=['POST'])
@api_require_login
def create_reservation(current_user):
    """
    Creates a new reservation (order) for the current user.
    This is a transactional operation: it either fully succeeds or fails completely.

    Expected JSON body:
    {
        "cafeteria_id": 1,
        "items": [
            { "dish_id": 1, "quantity": 1, "is_takeaway": false },
            { "dish_id": 4, "quantity": 2, "is_takeaway": true }
        ]
    }
    """
    data = request.get_json()
    if not data or not data.get('cafeteria_id') or not data.get('items'):
        return jsonify({"error": "Missing cafeteria_id or items list in request body."}), 400

    items_data = data['items']
    if not isinstance(items_data, list) or not items_data:
        return jsonify({"error": "The 'items' field must be a non-empty list."}), 400

    try:
        # --- 1. Validation and Cost Calculation ---
        total_cost = Decimal('0.0')
        order_details = []

        for item in items_data:
            dish = Dish.get_by_id(item.get('dish_id'))
            if not dish:
                # If any dish is invalid, fail the entire transaction
                db.session.rollback()
                return jsonify({"error": f"Dish with ID {item.get('dish_id')} not found."}), 404
            
            quantity = int(item.get('quantity', 1))
            if quantity <= 0:
                return jsonify({"error": f"Quantity for dish '{dish.name}' must be positive."}), 400

            price = Decimal(dish.dine_in_price)
            total_cost += price * quantity
            order_details.append({
                "dish_id": dish.dish_id,
                "quantity": quantity,
                "is_takeaway": bool(item.get('is_takeaway', False)),
                "applied_price": price
            })
        
        # --- 2. Check User Balance ---
        if current_user.balance < total_cost:
            return jsonify({
                "error": "Insufficient balance.",
                "required_balance": float(total_cost),
                "current_balance": float(current_user.balance)
            }), 402  # 402 Payment Required is a fitting status code

        # --- 3. Create Reservation and Order Items in a Transaction ---
        # Create the main reservation record
        new_reservation = Reservation.create_reservation(
            user_id=current_user.user_id,
            cafeteria_id=data['cafeteria_id'],
            total=total_cost,
            status='pending'  # Orders start as pending until fulfilled
        )
        db.session.add(new_reservation)
        db.session.flush()  # Assigns an ID to new_reservation without committing

        # Create the individual order items linked to the reservation
        for detail in order_details:
            OrderItem.create_order_item(
                reservation_id=new_reservation.reservation_id,
                **detail  # Unpacks the dictionary into arguments
            )

        # --- 4. Deduct from User's Balance ---
        current_user.balance -= total_cost
        
        # --- 5. Commit the Transaction ---
        db.session.commit()
        
        return jsonify(new_reservation.to_dict()), 201  # 201 Created

    except Exception as e:
        db.session.rollback()  # Roll back all changes if any error occurs
        return jsonify({"error": "An internal error occurred while creating the reservation.", "details": str(e)}), 500


@reservation_bp.route('/', methods=['GET'])
@api_require_login
def get_user_reservations(current_user):
    """
    Get the current user's full reservation history, newest first.
    (This functionality is moved from the main controller for better organization).
    """
    reservations = Reservation.query.filter_by(user_id=current_user.user_id).order_by(Reservation.reservation_datetime.desc()).all()
    
    # We create a more detailed dictionary for the response
    reservations_data = []
    for r in reservations:
        data = r.to_dict()
        data['order_items'] = [item.to_dict() for item in r.order_items]
        reservations_data.append(data)

    return jsonify(reservations_data), 200


@reservation_bp.route('/<int:reservation_id>', methods=['GET'])
@api_require_login
def get_single_reservation(current_user, reservation_id):
    """
    Get details for a single reservation. Ensures the user owns the reservation.
    """
    reservation = Reservation.get_by_id(reservation_id)

    if not reservation:
        return jsonify({"error": "Reservation not found."}), 404

    # Security check: User must own the reservation or be an admin
    if reservation.user_id != current_user.user_id and current_user.role != 'admin':
        return jsonify({"error": "Access forbidden. You do not own this reservation."}), 403

    # Add detailed order items to the response
    data = reservation.to_dict()
    data['order_items'] = [item.to_dict() for item in reservation.order_items]
    
    return jsonify(data), 200


@reservation_bp.route('/<int:reservation_id>/cancel', methods=['PUT'])
@api_require_login
def cancel_reservation(current_user, reservation_id):
    """
    Cancels a 'pending' reservation and refunds the amount to the user's balance.
    """
    reservation = Reservation.get_by_id(reservation_id)

    if not reservation:
        return jsonify({"error": "Reservation not found."}), 404

    if reservation.user_id != current_user.user_id:
        return jsonify({"error": "Access forbidden. You do not own this reservation."}), 403

    if reservation.status != 'pending':
        return jsonify({"error": f"Cannot cancel a reservation with status '{reservation.status}'. Only 'pending' orders can be cancelled."}), 409 # 409 Conflict

    try:
        # Refund the total amount to the user's balance
        current_user.balance += reservation.total
        
        # Update the reservation status
        reservation.status = 'cancelled'
        
        db.session.commit()
        
        return jsonify({
            "message": "Reservation cancelled successfully. Funds have been returned to your balance.",
            "reservation": reservation.to_dict(),
            "new_balance": float(current_user.balance)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An internal error occurred during cancellation.", "details": str(e)}), 500