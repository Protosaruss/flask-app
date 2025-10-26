from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecretkey"

# --- Veritabanı bağlantısı ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Kullanıcı Modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10))
    anon_name = db.Column(db.String(150))

# --- Ana Sayfa ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Kayıt Sayfası ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form.get("gender")
        anon_name = request.form.get("anon_name")

        # Anonim isim boşsa otomatik oluştur
        if not anon_name:
            anon_prefix = "Anon"
            gender_symbol = "♀" if gender == "Kadın" else "♂" if gender == "Erkek" else "⚧"
            anon_name = f"{anon_prefix}-{username[:3]}-{gender_symbol}"

        # Şifreyi hash’le
        hashed_pw = generate_password_hash(password, method="sha256")

        # Kullanıcıyı kaydet
        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            gender=gender,
            anon_name=anon_name
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Kayıt başarılı! Şimdi giriş yapabilirsin.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# --- Giriş Sayfası ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["anon_name"] = user.anon_name
            session["gender"] = user.gender
            flash("Giriş başarılı!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Geçersiz e-posta veya şifre.", "danger")
    return render_template("login.html")

# --- Dashboard ---
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Önce giriş yapmalısın!", "warning")
        return redirect(url_for("login"))

    anon_name = session.get("anon_name", "Anonim")
    gender = session.get("gender", "Belirsiz")
    return render_template("dashboard.html", anon_name=anon_name, gender=gender)

# --- Çıkış ---
@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("index"))

# --- Ana Çalıştırma ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
