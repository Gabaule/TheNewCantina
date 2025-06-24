from flask import Flask, render_template, request, session, redirect, url_for, g, flash
app = Flask(__name__)
app.secret_key = "supersecretdevstring"

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
    # Use date from query params or default
    selected_date = request.args.get("date") or "2024-01-15"
    current_cafeteria = CAFETERIAS[cafeteria_id]
    menu = MENUS[cafeteria_id]
    user = USERS[session["user_id"]]
    return render_template(
        "dashboard.html",
        cafeterias=CAFETERIAS,
        current_cafeteria=current_cafeteria,
        menu=menu,
        user=user,
        selected_date=selected_date,
    )

@app.route("/balance", methods=["GET", "POST"])
def balance():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = USERS[session["user_id"]]
    
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount > 0 and amount <= 500:  # Max top-up of $500
                USERS[session["user_id"]]["balance"] += amount
                flash(f"Successfully added ${amount:.2f} to your balance!", "success")
                return redirect(url_for("balance"))
            else:
                flash("Please enter an amount between $0.01 and $500.00", "error")
        except (ValueError, KeyError):
            flash("Invalid amount entered", "error")
    
    return render_template("balance.html", user=user)

