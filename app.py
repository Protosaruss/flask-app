<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Giriş Yap</title>
  <style>
    body {
      background: #0d0d0d; color: #fff; font-family: Arial, sans-serif;
      display: flex; align-items: center; justify-content: center;
      height: 100vh; margin: 0;
    }
    .card { background:#161616; padding:30px; border-radius:14px; width:320px; }
    h1 { text-align:center; margin-bottom:20px; }
    input, button { width:100%; padding:10px; border:none; border-radius:8px; }
    input { margin-bottom:12px; font-size:15px; }
    button { background:#ffcc00; color:#000; font-weight:700; cursor:pointer; }
    button:hover { background:#ffdb4d; }
    .flash { background:#2a2a2a; padding:8px; margin-bottom:10px; border-radius:8px; color:#ffcc00; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🔐 Giriş Yap</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="flash">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form method="POST" action="{{ url_for('login') }}">
      <input type="text" name="username" placeholder="Kullanıcı adı" required>
      <input type="password" name="password" placeholder="Şifre" required>
      <button type="submit">Giriş Yap</button>
    </form>

    <p style="margin-top:10px;text-align:center;">
      <a href="{{ url_for('register') }}" style="color:#ffcc00;">Hesabın yok mu? Kayıt ol</a>
    </p>
  </div>
</body>
</html>
