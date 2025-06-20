from flask import Flask, render_template, request, session, redirect, url_for, g
app = Flask(__name__)
app.secret_key = "supersecretdevstring"

# Example user data
USERS = {
    "student1": {"password": "pass123", "name": "John Doe", "type": "student"},
    "faculty1": {"password": "pass123", "name": "Dr. Smith", "type": "faculty"},
}

# Cafeteria data
CAFETERIAS = {
    "main": {
        "id": "main",
        "name": "Main Cafeteria",
        "description": "Our largest dining facility with diverse options"
    },
    "science": {
        "id": "science", 
        "name": "Science Building Cafe",
        "description": "Quick bites and coffee for busy students"
    },
    "library": {
        "id": "library",
        "name": "Library Food Court", 
        "description": "Quiet dining with healthy options"
    }
}

# Sample menu data for each cafeteria
MENUS = {
    "main": [
        {"name": "Grilled Chicken", "description": "Herb-seasoned grilled chicken breast", "price": "12.99"},
        {"name": "Veggie Burger", "description": "Plant-based patty with fresh vegetables", "price": "10.99"},
        {"name": "Caesar Salad", "description": "Fresh romaine with parmesan and croutons", "price": "8.99"},
        {"name": "Pasta Primavera", "description": "Seasonal vegetables with penne pasta", "price": "11.99"}
    ],
    "science": [
        {"name": "Coffee & Pastry", "description": "Fresh brewed coffee with daily pastry", "price": "5.99"},
        {"name": "Sandwich Combo", "description": "Deli sandwich with chips and drink", "price": "9.99"},
        {"name": "Energy Bowl", "description": "Quinoa bowl with nuts and berries", "price": "8.99"}
    ],
    "library": [
        {"name": "Green Smoothie", "description": "Spinach, banana, and protein blend", "price": "6.99"},
        {"name": "Quiet Wrap", "description": "Turkey and avocado in whole wheat", "price": "7.99"},
        {"name": "Study Snack Box", "description": "Mixed nuts, fruit, and crackers", "price": "4.99"},
        {"name": "Herbal Tea Set", "description": "Selection of calming herbal teas", "price": "3.99"}
    ]
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username]["password"] == password:
            session["user_id"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
@app.route("/dashboard/<cafeteria_id>")
def dashboard(cafeteria_id="main"):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Validate cafeteria_id
    if cafeteria_id not in CAFETERIAS:
        cafeteria_id = "main"
    
    current_cafeteria = CAFETERIAS[cafeteria_id]
    menu = MENUS[cafeteria_id]
    user = USERS[session["user_id"]]
    
    return render_template("dashboard.html", 
                         cafeterias=CAFETERIAS,
                         current_cafeteria=current_cafeteria,
                         menu=menu,
                         user=user,
                         selected_date="2024-01-15")

if __name__ == "__main__":
    app.run(debug=True)