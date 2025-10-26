from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Şimdilik gelen bilgileri terminale yazdıralım (test amaçlı)
    print(f"Yeni kullanıcı kaydı: {username} - {email} - {password}")

    # Geçici olarak teşekkür sayfası gösterelim
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
