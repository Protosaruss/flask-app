from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# --- Render PostgreSQL bağlantısı ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- Kullanıcı Modeli ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20))

# --- Ana Sayfa ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Kayıt ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        gender = request.form['gender']

        if User.query.filter_by(username=username).first():
            flash("Bu kullanıcı adı zaten alınmış.", "error")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Bu e-posta zaten kayıtlı.", "error")
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password, gender=gender)
        db.session.add(new_user)
        db.session.commit()

        flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# --- Giriş ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("E-posta veya şifre hatalı.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

# --- Dashboard ---
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

# --- Uygulama başlatma ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
