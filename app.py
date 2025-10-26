from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

# --- Güvenlik ve DB ayarları ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey_change_me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Lütfen önce giriş yapın.'

# --- Model ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Uygulama başlarken tabloyu oluştur
with app.app_context():
    db.create_all()

# --- Sayfalar ---
@app.route('/')
def home():
    # mevcut index.html’in kalsın (görsel burada)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        raw_password = request.form.get('password', '')
        if not username or not email or not raw_password:
            flash('Lütfen tüm alanları doldurun.', 'danger')
            return redirect(url_for('register'))

        # e-posta veya kullanıcı adı zaten var mı?
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Bu kullanıcı adı veya e-posta zaten kayıtlı.', 'warning')
            return redirect(url_for('register'))

        hashed = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        raw_password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, raw_password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('E-posta veya parola hatalı.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Render/gunicorn için app nesnesi yeterli; local test:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
