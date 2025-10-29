# ------------------------------------------------------
# app.py – MySecretIsYourSecret (Render için güvenli sürüm)
# ------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

# --- Flask Başlatma ---
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Render PostgreSQL bağlantısı ---
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://flask_db_gvdu_user:Aob8bxDlwlCqmQYLs3kexSuHMOOvY8Dd"
    "@dpg-d3vkonjipnbc739o4po0-a/flask_db_gvdu?sslmode=require"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Veritabanı ---
db = SQLAlchemy(app)

# --- Kullanıcı Modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

# --- Sır Modeli ---
class Secret(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --- Veritabanı oluştur ---
with app.app_context():
    db.create_all()

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
            return redirect(url_for('secrets'))
        else:
            flash("Kullanıcı adı veya şifre hatalı.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# --- Sırlar Sayfası ---
@app.route('/secrets', methods=['GET', 'POST'])
def secrets():
    if 'user' not in session:
        flash("Lütfen önce giriş yapın.", "error")
        return redirect(url_for('login'))

    username = session['user']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        content = request.form.get('content')
        if not content or not content.strip():
            flash("Boş sır gönderemezsiniz.", "error")
            return redirect(url_for('secrets'))

        new_secret = Secret(content=content, user_id=user.id)
        db.session.add(new_secret)
        db.session.commit()
        flash("Sırrınız başarıyla paylaşıldı!", "success")
        return redirect(url_for('secrets'))

    all_secrets = Secret.query.order_by(Secret.id.desc()).all()
    return render_template('secrets.html', secrets=all_secrets)

# --- Çıkış ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('home'))

# --- Çalıştırma ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
