from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# --- Flask uygulaması oluşturma ---
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Render PostgreSQL bağlantısı ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_db_gvdu_user:Aob8bxDlwlCqmQYLs3kexSuHMOOvY8Dd@dpg-d3vkonjipnbc739o4po0-a/flask_db_gvdu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Veritabanı ve şifreleme ayarları ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# --- Kullanıcı modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email, password, gender):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.gender = gender


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

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Bu kullanıcı adı veya e-posta zaten alınmış.", "error")
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password, gender=gender)
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


# --- Kullanıcı paneli (Dashboard) ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
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


# --- Veritabanı oluşturma komutu ---
@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("✅ Veritabanı oluşturuldu!")


# --- Uygulama başlatma ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
