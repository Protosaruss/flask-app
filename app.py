from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Render debug modda çalışmaz, True yerine False olmalı
    app.run(host="0.0.0.0", port=5000)
