from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# --- Flask uygulaması ---
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Render PostgreSQL bağlantısı ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_db_gvdu_user:YOUR_PASSWORD@dpg-d3vkonjipnbc739o4po0-a/flask_db_gvdu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- Kullanıcı modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

# --- Ana sayfa ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Kayıt sayfası ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']

        # Kullanıcı zaten var mı?
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Bu kullanıcı adı veya e-posta zaten alınmış.", "error")
            return redirect(url_for('register'))

        # Şifreyi hashle
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw, gender=gender)

        db.session.add(new_user)
        db.session.commit()

        flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# --- Giriş sayfası ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.username
            flash("Giriş başarılı!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("E-posta veya şifre hatalı.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# --- Kullanıcı paneli ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Lütfen giriş yapın.", "error")
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

# --- Veritabanını başlatma (sadece ilk kez çalıştırırken) ---
@app.cli.command("create-db")
def create_db():
    """Veritabanı tablolarını oluşturur"""
    db.create_all()
    print("✅ Veritabanı oluşturuldu!")

# --- Sunucu başlat ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
