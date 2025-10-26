from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Basit bir kullanıcı listesi (geçici veri deposu)
users = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    gender = request.form["gender"]

    # Kullanıcıyı listeye ekle
    user = {
        "username": username,
        "email": email,
        "password": password,
        "gender": gender
    }
    users.append(user)

    # Session'a kaydet
    session["user"] = username
    session["gender"] = gender

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    user = session["user"]
    gender = session["gender"]

    # Cinsiyet simgesi seçimi
    if gender == "male":
        symbol = "👨"
    elif gender == "female":
        symbol = "👩"
    else:
        symbol = "⚧️"

    return render_template("dashboard.html", user=user, gender_symbol=symbol)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("gender", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
