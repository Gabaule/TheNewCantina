# app/controller/auth.py

from functools import wraps
from flask import session, jsonify, redirect, url_for, flash
from models import AppUser

def get_current_user():
    """Helper to get the currently logged-in user object from session."""
    if "user_id" in session:
        print(f"[DEBUG] ✅ Found 'user_id' in session: {session['user_id']}. Access granted.")
        return AppUser.get_by_id(session["user_id"])
    else:
        print("[DEBUG] ❌ 'user_id' NOT found in session. Redirecting to login page.")
    return None

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

def require_login():
    """Helper function to protect web pages, redirects if not logged in."""
    if "user_id" not in session:
        flash("Vous devez être connecté pour accéder à cette page.", "warning")
        return redirect(url_for("login"))
    return None

def api_require_login(f):
    """Decorator for API routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentification requise. Veuillez vous connecter."}), 401
        
        user = get_current_user()
        if not user:
            session.clear()
            return jsonify({"error": "Utilisateur non trouvé. Veuillez vous reconnecter."}), 401
        
        # Pass the user object to the decorated function
        return f(current_user=user, *args, **kwargs)
    return decorated_function