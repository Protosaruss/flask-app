# ============================================================
# app.py — MySecretIsYourSecret Flask Uygulaması (Render için)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

# --- Flask Uygulaması Başlatma ---
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Render PostgreSQL Bağlantısı ---
# Render'daki "External Database URL" değerini buraya ekle
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://flask_db_gvdu_user:Aob8bxDlwlCqmQYLs3kexSuHMOOvY8Dd@dpg-d3vkonjipnbc739o4po0-a/flask_db_gvdu"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Veritabanı Nesnesi ---
db = SQLAlchemy(app)

# --- Kullanıcı Modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

# --- Veritabanı Oluşturma (Render’da otomatik olsun) ---
with app.app_context():
    db.create_all()

# ============================================================
# ROTALAR
# ============================================================

# --- Ana Sayfa ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Kayıt Sayfası ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')

        if not username or not email or not password or not gender:
            flash("Lütfen tüm alanları doldurun.", "error")
            return redirect(url_for('register'))

        try:
            new_user = User(username=username, email=email, password=password, gender=gender)
            db.session.add(new_user)
            db.session.commit()
            flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("Bu kullanıcı adı veya e-posta zaten kayıtlı.", "error")
            return redirect(url_for('register'))

    return render_template('register.html')

# --- Giriş Sayfası ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Lütfen tüm alanları doldurun.", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = user.username
            flash("Başarıyla giriş yaptınız!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Kullanıcı adı veya şifre hatalı.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# --- Kullanıcı Paneli (Dashboard) ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Lütfen önce giriş yapın.", "error")
        return redirect(url_for('login'))

    username = session['user']
    user = User.query.filter_by(username=username).first()
    gender_icon = "♂️" if user.gender == "Erkek" else "♀️" if user.gender == "Kadın" else "⚧️"

    return render_template('dashboard.html', username=username, gender_icon=gender_icon)

# --- Çıkış ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('home'))

# ============================================================
# Uygulama Çalıştırma (Render uyumlu)
# ============================================================
if __name__ == '__main__':
    # Render ortamında 0.0.0.0 host gereklidir
    app.run(host='0.0.0.0', port=5000)
