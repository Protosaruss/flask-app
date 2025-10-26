from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import os

app = Flask(__name__)

# --- Veritabanı bağlantısı ---
DB_PATH = "users.db"

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            print("📁 Veritabanı oluşturuldu: users.db")

init_db()

# --- Ana sayfa ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Kayıt formu işlemi ---
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Boş alan kontrolü
    if not username or not email or not password:
        return "⚠️ Lütfen tüm alanları doldurun.", 400

    # Veritabanına kaydet
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, password))
        conn.commit()

    print(f"✅ Yeni kullanıcı eklendi: {username} ({email})")

    return f"""
    <html>
    <head><title>Kayıt Başarılı</title></head>
    <body style='background-color:#0d0d0d; color:#fff; text-align:center; font-family:Arial;'>
        <h1>✅ Kayıt Başarılı!</h1>
        <p>Hoş geldin, <strong>{username}</strong>!</p>
        <p><a href='/' style='color:#ffcc00;'>Ana Sayfaya Dön</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
