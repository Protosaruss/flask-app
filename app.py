from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"

# --- Veritabanı bağlantısı ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

# --- Kullanıcı Modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    anon_name = db.Column(db.String(80), nullable=False)

# --- Ana Sayfa ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Kayıt Sayfası ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]
        anon_name = request.form["anon_name"]

        # Yeni kullanıcı oluştur
        new_user = User(username=username, email=email, password=password,
                        gender=gender, anon_name=anon_name)

        db.session.add(new_user)
        db.session.commit()

        session["user"] = username
        session["anon_name"] = anon_name
        session["gender"] = gender
        return redirect(url_for("dashboard"))
    return render_template("register.html")

# --- Giriş Sayfası ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user"] = user.username
            session["anon_name"] = user.anon_name
            session["gender"] = user.gender
            return redirect(url_for("dashboard"))
        else:
            return "Hatalı giriş!"
    return render_template("login.html")

# --- Dashboard (Kullanıcı Paneli) ---
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        gender = session.get("gender", "")
        symbol = "👨" if gender == "male" else "👩" if gender == "female" else "⚧"
        return render_template("dashboard.html",
                               anon_name=session["anon_name"],
                               gender_symbol=symbol)
    return redirect(url_for("login"))

# --- Çıkış ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# --- Ana Uygulama ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
