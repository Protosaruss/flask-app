from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Veritabanı bağlantısı ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Kullanıcı modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# --- Ana sayfa ---
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Yeni kullanıcı oluştur
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # veritabanını oluşturur
    app.run(debug=True)
