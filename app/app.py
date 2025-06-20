from flask import Flask, render_template, request, session, redirect, url_for, g

app = Flask(__name__)
app.secret_key = "supersecretdevstring"

# Example user data
USERS = {
    "student1": {"password": "pass123", "name": "John Doe", "type": "student"},
    "faculty1": {"password": "pass123", "name": "Dr. Smith", "type": "faculty"},
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username]["password"] == password:
            session["user_id"] = username
            return redirect(url_for("index"))  # or dashboard/home
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
    return f"Welcome, {USERS[session['user_id']]['name']}!"  


if __name__ == "__main__":
    app.run(debug=True)