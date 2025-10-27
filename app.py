from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Render ve Flask için dizin ayarları ---
app.template_folder = os.path.join(os.path.dirname(__file__), 'templates')
app.static_folder = os.path.join(os.path.dirname(__file__), 'static')

# --- Sahte veri tabanı (örnek olarak RAM'de tutuluyor) ---
users = {}

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

        # Aynı e-posta veya kullanıcı adı kayıtlı mı?
        for user, data in users.items():
            if data["email"] == email:
                flash("Bu e-posta adresiyle zaten bir hesap var.", "error")
                return redirect(url_for('register'))
        if username in users:
            flash("Bu kullanıcı adı zaten alınmış.", "error")
            return redirect(url_for('register'))

        users[username] = {"email": email, "password": password, "gender": gender}
        flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# --- Giriş sayfası (e-posta ile giriş) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # E-posta üzerinden kullanıcıyı bul
        for user, data in users.items():
            if data["email"] == email and data["password"] == password:
                session['user'] = user
                return redirect(url_for('dashboard'))

        flash("E-posta veya şifre hatalı.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

# --- Kullanıcı paneli (Dashboard) ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    user_gender = users[username]["gender"]
    gender_icon = "♂️" if user_gender == "Erkek" else "♀️" if user_gender == "Kadın" else "⚧️"

    return render_template('dashboard.html', username=username, gender_icon=gender_icon)

# --- Çıkış ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for('home'))

# --- Uygulama çalıştırma ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
