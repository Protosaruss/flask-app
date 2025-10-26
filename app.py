from flask import Flask, render_template, request
import random

app = Flask(__name__)

# --- Anonim isim oluşturucu ---
anon_prefixes = ["Mavi", "Gizli", "Karanlık", "Tatlı", "Uçan", "Sır", "Gece", "Rüya", "Gölge", "Sessiz"]
anon_suffixes = ["Kuş", "Yıldız", "Kalp", "Bulut", "Kedi", "Düş", "Fısıltı", "Kurt", "Ay", "Deniz"]

def generate_anon_name():
    return random.choice(anon_prefixes) + random.choice(anon_suffixes)

# --- Ana sayfa (kayıt ekranı) ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Kayıt formu gönderimi ---
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    gender = request.form["gender"]

    # Rastgele anonim isim oluştur
    anon_name = generate_anon_name()

    # Cinsiyet simgesi seçimi
    icons = {"male": "👨", "female": "👩", "other": "🧑"}
    gender_icon = icons.get(gender, "🧑")

    # Dashboard’a yönlendir
    return render_template("dashboard.html", anon_name=anon_name, gender_icon=gender_icon)

# --- Dashboard (giriş sonrası ekran) ---
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", anon_name="Anonim", gender_icon="🧑")

if __name__ == "__main__":
    app.run(debug=True)
