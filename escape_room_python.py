# -*- coding: utf-8 -*-
# Escape Room web app (Flask) - "El Misterio de Nuestro Amor"
# Instalación: pip install flask
# Ejecutar: python escape_room_python.py

from flask import Flask, request, render_template_string, redirect, url_for, session
import os

app = Flask(__name__)
# Necesitas una clave secreta para la gestión de la sesión
app.secret_key = 'tu_clave_secreta_aqui_cambiala' 

# ==============================================================================
#                               CONFIGURACIÓN
# ==============================================================================

SECRET_CODE_1 = "Fira"   # Código para la primera prueba
SECRET_CODE_2 = "KAROTTE"  # Código para la segunda prueba
SECRET_CODE_3 = "1033,5" # Código para la tercera prueba. Ahora es un número!
SECRET_CODE_5 = "Passeig dels Til·lers" # NUEVO: Código para la quinta prueba (Morse).
SECRET_CODE_6 = "23" # NUEVO: Código para la sexta prueba (coordenada). CÁMBIALO!
SECRET_CODE_7 = "3" # NUEVO: Código para la prueba del Café/Torre. CÁMBIALO!
SECRET_CODE_8 = "SAGRADA FAMILIA" # NUEVO: Código para la prueba del acertijo.
SECRET_CODE_9 = "Amen" # NUEVO: Código final in-situ de la Sagrada Familia. CÁMBIALO!
SECRET_CODE_10 = "Estrella"
SECRET_CODE_11 = "44"
SECRET_CODE_12 = "2" # Código final (opcional)
 # NUEVO: Imagen para la prueba del Café/Torre
MUSIC_FILE = "x.mp3"      # archivo de música en static/

# Archivos de Imagen (Deben existir en la carpeta static/!)
BG_IMAGE_FILE_INTRO = "primer_fondo.png"
BG_IMAGE_FILE_1 = "photo.jpg"
BG_IMAGE_FILE_2 = "photo 2.jpg"
BG_IMAGE_FILE_3 = "photo.jpg"
BG_IMAGE_FILE_4 = "photo 2.jpg"
BG_IMAGE_FILE_ACTION = "photo.jpg"
BG_IMAGE_FILE_6 = "photo 2.jpg"
BG_IMAGE_FILE_7 = "top.jpg" 

BG_IMAGE_FILE_8 = "photo.jpg" # NUEVO: Fondo para la prueba 8 (Acertijo de Gaudí)
BG_IMAGE_FILE_9 = "photo 2.jpg" # NUEVO: Fondo para la prueba 9 (in-situ)
BG_IMAGE_FILE_10 = "photo.jpg"
BG_IMAGE_FILE_11 = "photo 2.jpg"
BG_IMAGE_FILE_12 = "photo.jpg"
BINARY_IMAGE_FILE = "image_77469a.jpg"
MORSE_MANUAL_IMAGE_FILE = "morse11.jpg"
cafe_image_file = "top.jpg" 
GENERIC_TEMPLATE_STYLE = '''
<style>
  html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  /* ... resto del código CSS de estilo ... */
  .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
  .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
</style>
'''

GENERIC_TEMPLATE_SCRIPT = '''
<audio id="bgMusic" loop>
  <source src="/static/{{ music_file }}" type="audio/mpeg">
  Tu navegador no soporta audio en HTML5.
</audio>
<script>
  const music = document.getElementById('bgMusic');
  music.volume = 0.15;
  music.play();
</script>
'''

# ==============================================================================
#                               PLANTILLAS HTML
# ==============================================================================

# Plantilla para la página de introducción
INTRO_TEMPLATE = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Nuestra Aventura</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .start-btn { padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer; transition:transform 0.2s ease; }
    .start-btn:hover { transform:scale(1.05); }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      <h1>💖 FELICIDADES AMOR 💖</h1>
      <p>Bienvenida a un viaje lleno de recuerdos, misterios y amor! Efectivamente has acertado mi regalo porque eres la más lista jeje. He creado este juego para que revivamos juntos algunos de los momentos más especiales.</p>
      <p>Resuelve cada enigma para descubrir la siguiente pista y encontrar tu regalo especial. Tu misión comienza ahora!</p>
      <a href="{{ url_for('first_puzzle') }}"><button class="start-btn">Comenzar Aventura ➡️</button></a>
    </div>
  </div>
  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>
  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15; // volumen bajo
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la primera prueba
TEMPLATE_1 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Primer Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: #003681;  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .hint { margin-top:20px; font-size:16px; opacity:0.95; }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
    footer { margin-top:24px; font-size:14px; opacity:0.9; }
    #startBtn { position:absolute; top:10px; right:10px; padding:12px 18px; font-size:16px; border-radius:8px; background:#ffeb3b; color:#111; border:none; cursor:pointer; font-weight:700; }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>💖✨ Nuestro misterio ✨💖</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Correcto! 🎉</strong>
          <p>¿Fácil no? Fue después de dar una vuelta en el Golfito jeje</p>
            <img src="/static/recuerdo.jpg" alt="recuerdo" style="max-width:320px; margin:18px auto 0 auto; display:block; border-radius:14px; box-shadow:0 4px 18px rgba(0,0,0,0.18);">
            <a href="{{ url_for('next_page_2') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Siguiente pista ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>No es correcto 😢</strong>
          <p>Vuelve a intentarlo o usa la pista si la necesitas.</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>{{ intro_text }}</p>
        <form method="POST" action="{{ url_for('submit_1') }}">
          <input type="text" name="code" placeholder="Escribe aquí tu respuesta..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
        
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15; // volumen bajo
    music.play();
  </script>

</body>
</html>
'''

# Plantilla para la segunda prueba
TEMPLATE_2 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Segundo Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; flex-direction: column; align-items:center; justify-content:center; }
    .overlay { background: rgba(255, 255, 255, 0.9);  padding:40px; border-radius:20px; color:#111; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.15); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:42px; color:#4a148c; }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:18px; }
    .puzzle-grid { display: flex; flex-direction: column; gap: 20px; align-items: center; margin-bottom: 25px; }
    .text-block { background: #e0f7fa; padding: 25px; border-left: 5px solid #00bcd4; text-align: left; font-style: italic; border-radius: 8px; flex: 1; }
    .image-block { flex: 1; max-width: 100%; text-align: center; }
    .binary-image { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .binary-code-text { background: #111; color: #0f0; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 20px; letter-spacing: 2px; text-align: center; overflow-x: auto; white-space: nowrap; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:2px solid #ccc; font-size:18px; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#4a148c; color:#fff; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
    @media (min-width: 768px) {
      .puzzle-grid { flex-direction: row; align-items: flex-start; }
      .text-block, .image-block { flex: 1; }
    }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨Prueba 2: El Enigma Binario ✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Correcto! 🎉</strong>
          <p>Eres una genia con los ordenadores! Saca la calcu para la siguiente prueba que se vienen números.</p>
          <a href="{{ url_for('next_page_3') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#4a148c; color:#fff; font-weight:700; font-size:18px; cursor:pointer;">Siguiente pista ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>No es correcto 😢</strong>
          <p>Vuelve a leer la historia con atención.</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <div class="puzzle-grid">
          <div class="text-block">
            <p>Te he dejado un mensaje. Es el código que abre la puerta a la siguiente pista, pero está escrito en el lenguaje de las máquinas que estoy estudiando. Para descifrarlo, tendrás que entender cómo piensan los ordenadores.</p>
            <p>Cada grupo de 8 bits (ocho ceros y unos) representa una letra, un número o un símbolo. A continuación, te he dejado una tabla para que puedas descifrar el mensaje secreto.</p>
          </div>
          <div class="image-block">
            <img src="/static/{{ binary_image_file }}" alt="Código Binario" class="binary-image">
          </div>
        </div>
        
        <p><b>El Mensaje Secreto:</b></p>
        <div class="binary-code-text">{{ binary_text }}</div>

        <form method="POST" action="{{ url_for('submit_2') }}">
          <input type="text" name="code" placeholder="Escribe el nombre aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>

</body>
</html>
'''

# Plantilla para la tercera prueba (Enigma numérico y personal)
TEMPLATE_3 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Tercer Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:600px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    ul { list-style-type: none; padding: 0; margin: 20px auto; max-width: 400px; text-align: left; }
    li { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 10px; font-size: 18px; }
    .math-symbol { font-size: 2.5em; font-weight: bold; color: #ffeb3b; text-align: center; margin: 10px 0; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ Prueba 3: El Enigma del Número ✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>De locotron! 🎉</strong>
          <p>Vas muy bien, sigue así!!!.</p>
          <a href="{{ url_for('start_puzzle_4') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Siguiente pista ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>No es correcto 😢</strong>
          <p>Vuelve a pensarlo bien. Los números no mienten!</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Resuelve el siguiente acertijo matemático para encontrar la clave:</p>
        <ul>
          <li>1. ¿Cuántos meses llevamos juntos? </li>
          <div class="math-symbol">×</div>
          <li>2. ¿Cuántas temporadas de Big Bang Theory vamos a ver? </li>
          <div class="math-symbol">+</div>
          <li>3. Suma tu año de nacimiento + tu numero de mes + tu dia de nacimiento</li>
          <div class="math-symbol">/</div>
          <li>4. ¿La primera noche que dormimos juntos en tu casa? (solo el día de esa fecha)</li>
          <div class="math-symbol">-</div>
          <li>5. ¿Tu dorsal + el mío sumados? </li>
        </ul>
        <p>¿Cuál es el número final?</p>
        <form method="POST" action="{{ url_for('submit_3') }}">
          <input type="text" name="code" placeholder="Escribe tu respuesta..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>

</body>
</html>
'''

# Plantilla para la cuarta prueba (Acertijo de la Sangría de Salts)
TEMPLATE_4 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 El Misterio de la Sangría</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .vessels-container { display:flex; justify-content:center; gap:30px; margin:40px 0; }
    .vessel { position:relative; width:150px; height:250px; border:4px solid #fff; border-radius:10px; background: rgba(255,255,255,0.2); overflow:hidden; }
    .vessel.jarra { height:200px; width:120px; }
    .liquid { position:absolute; bottom:0; width:100%; background: #962800; transition:height 0.5s ease-in-out; }
    .label { position:absolute; bottom:10px; left:50%; transform:translateX(-50%); color:#ffc107; font-size:20px; font-weight:bold; }
    .actions { display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin-top:30px; }
    .actions button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:16px; transition:transform 0.2s ease; }
    .actions button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; margin-top:20px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; margin-top:20px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨Prueba 4: El Misterio de la Sangría de Salts ✨</h1>
      {% if message %}
        <div class="{{ 'success' if 'Felicidades!' in message else 'error' }}">
          <strong>{{ message }}</strong>
        </div>
      {% endif %}

      {% if not puzzle_solved %}
        <p>En el bar necesitais conseguir 4 litros de sangría exactos. El problema es que solo tenéis un recipiente de 5 litros y un recipiente de 3 litros. Ahora entiendes lo de la jungla de cristal jajaja</p>

        <div class="vessels-container">
          <div class="vessel">
            <div class="liquid" style="height:{{ (vessels['v5'] / 5) * 100 }}%;"></div>
            <div class="label">{{ vessels['v5'] }}L / 5L</div>
          </div>
          <div class="vessel jarra">
            <div class="liquid" style="height:{{ (vessels['v3'] / 3) * 100 }}%;"></div>
            <div class="label">{{ vessels['v3'] }}L / 3L</div>
          </div>
        </div>

        <div class="actions">
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="fill5">
            <button type="submit">Llenar 5L</button>
          </form>
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="fill3">
            <button type="submit">Llenar 3L</button>
          </form>
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="empty5">
            <button type="submit">Vaciar 5L</button>
          </form>
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="empty3">
            <button type="submit">Vaciar 3L</button>
          </form>
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="pour5to3">
            <button type="submit">Pasar 5L a 3L</button>
          </form>
          <form method="POST" action="{{ url_for('submit_4') }}">
            <input type="hidden" name="action" value="pour3to5">
            <button type="submit">Pasar 3L a 5L</button>
          </form>
        </div>
      {% else %}
        <div class="success">
          <strong>Lo lograste! 🎉</strong>
          <p>La Sangría perfecta ha sido creada. </p>
          <a href="{{ url_for('start_action') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Siguiente ➡️</button></a>
        </div>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>

</body>
</html>
'''

# Plantilla para la página de "Paso a la Acción"
ACTION_TEMPLATE = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Pasamos a la Acción! 🚀</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .coordinates { font-size: 2.5em; font-weight: bold; margin: 40px 0; color: #fff; letter-spacing: 2px; }
    .start-btn { padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer; transition:transform 0.2s ease; }
    .start-btn:hover { transform:scale(1.05); }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} .coordinates{font-size:1.8em;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      <h1>Pasamos a la Acción! 🚀</h1>
      <p>¿Difícil?, chill que ahora empieza lo bueno jajaja. Coge el casco que vamos a dar una vuelta por la city jeje. Lo que vas a ver abajo son las coordenadas del final del juego. Como puedes ver, faltan algunos numeros por rellenar. A medida que vayas resolviendo los siguientes acertijos, conseguirás completar la ubicación del lugar final. Recuerda: Los símbolos faltantes pueden ser números o letras. READY??? Te he dejado en la siguiente pantalla el nombre de la calle encriptado, resuelvelo y arranca motores que nos vamos!!! </p>
      
      <p><b>Destino Final:</b></p>
      <p class="coordinates">
        41°?'44.?"? 2°09'08.?"?"
      </p>

      <a href="{{ url_for('puzzle_5') }}"><button class="start-btn">Siguiente prueba ➡️</button></a>
    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la quinta prueba (Morse)
TEMPLATE_5 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Quinto Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:880px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .puzzle-content { display: flex; flex-direction: column; align-items: center; gap: 20px; margin: 40px 0; }
    .morse-text { font-size: 1.5em; font-weight: bold; color: #fff; letter-spacing: 3px; word-break: break-all; }
    .morse-manual-img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    @media (min-width: 768px) {
      .puzzle-content { flex-direction: row; justify-content: center; align-items: flex-start; }
      .text-container { flex: 1; text-align: left; }
      .image-container { flex: 1; text-align: right; }
    }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ Rompecabezas de la Calle ✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Correcto! 🎉</strong>
          <p>Has descubierto el nombre de la calle! Toca ir allí para descubrir tu primera coordenada.</p>
          <a href="{{ url_for('puzzle_6') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">A la siguiente pista! ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>No es correcto 😢</strong>
          <p>Vuelve a pensarlo. Los puntos y rayas tienen un mensaje oculto!</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Decodifica el siguiente mensaje en código morse para encontrar el nombre de la calle. Usa el manual para ayudarte(No es relevante la altura a la que estén los puntos):</p>
        <div class="puzzle-content">
          <div class="text-container">
            <div class="morse-text">{{ morse_text }}</div>
          </div>
          <div class="image-container">
            <img src="/static/{{ morse_manual_image_file }}" alt="Manual de Código Morse" class="morse-manual-img">
          </div>
        </div>
        <form method="POST" action="{{ url_for('submit_5') }}">
          <input type="text" name="code" placeholder="Escribe el nombre de la calle aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>

</body>
</html>
'''

# Plantilla para la sexta prueba (Número de casa)
TEMPLATE_6 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Sexto Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:600px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.2em; font-style: italic; margin-bottom: 30px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨El número de la casa!✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Increíble! 🎉</strong>
          <p>Has encontrado el número correcto. Guarda este primer bloque, te sera útil para el final (41°{{ secret_code }}')</p>
          <a href="{{ url_for('next_page_7') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Siguiente prueba ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Número incorrecto 😢</strong>
          <p>Vuelve a pensarlo bien. No es el número de la casa en la que vivimos sino la de las coordenadas</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Has encontrado la calle! Lo primero que debes hacer es sacarte un selfie con tu novio, es crucial para el juego jejeje. Ahora necesitas el número. Piensa bien que número será el correcto. Cuando lo hayas encontrado, réstale el número del dia que nació tu novio y ya tendrás un bloque de las coordenadas hecho.</p>
        <p class="riddle-text">
        El primer número que falta de las coordenadas es...
        </p>
        <form method="POST" action="{{ url_for('submit_6') }}">
          <input type="text" name="code" placeholder="Escribe el número aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la séptima prueba (Café/Torre)
# Reemplaza los TEMPLATE_7_IN_SITU y TEMPLATE_7_ACTION en tu código
# con estas dos nuevas plantillas:

# Plantilla para la SÉPTIMA PRUEBA (Parte 1: Ir al lugar - Diseño Unificado)
TEMPLATE_7_IN_SITU = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Hora de Moverse! 📍</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:650px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .warning { color:#fff; background:rgba(255, 0, 0, 0.6); padding:10px; border-radius:8px; margin-bottom:20px; font-weight:bold; }
    .location-image { max-width: 90%; height: auto; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .next-btn { padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer; transition:transform 0.2s ease; }
    .next-btn:hover { transform:scale(1.05); }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ Misión diagonal✨</h1>
      <p>Es hora de demostrar que tienes sentido de la orientación! Tienes que ir al lugar que aparece en esta foto.ATENCIÓN! Si usas Google Maps o cualquier otra aplicación de navegación, el regalo se cancela inmediatamente.</p>
      
      <div class="warning">
        ⛔ **ADVERTENCIA: CERO MAPAS!** ⛔
      </div>
      
      <img src="/static/{{ cafe_image_file }}" alt="Ubicación del café" class="location-image">
      
      <p>Cuando llegues al lugar, pulsa el botón para recibir la siguiente instrucción:</p>
      
      <a href="{{ url_for('go_to_cafe') }}"><button class="next-btn">✅ Ya he llegado</button></a>
    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la SÉPTIMA PRUEBA (Parte 2: Acción en la azotea - Diseño Unificado)
# Plantilla para la SÉPTIMA PRUEBA (Parte 1: Ir al lugar - Diseño Unificado)
TEMPLATE_7_IN_SITU = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Hora de Moverse! 📍</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:650px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .warning { color:#fff; background:rgba(255, 0, 0, 0.6); padding:10px; border-radius:8px; margin-bottom:20px; font-weight:bold; }
    .location-image { max-width: 90%; height: auto; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .next-btn { padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer; transition:transform 0.2s ease; }
    .next-btn:hover { transform:scale(1.05); }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ Misión en Vivo: El Café! ✨</h1>
      <p>Es hora de demostrar que tienes sentido de la orientación! Tienes que ir al lugar que aparece en esta foto. **ATENCIÓN! Si usas Google Maps o cualquier otra aplicación de navegación, el regalo se cancela inmediatamente.** </p>
      
      <div class="warning">
        ⛔ **ADVERTENCIA: CERO MAPAS!** ⛔
      </div>
      
      <img src="/static/{{ cafe_image_file }}" alt="Ubicación del café" class="location-image">
      
      <p>Cuando llegues al lugar, pulsa el botón para recibir la siguiente instrucción:</p>
      
      <a href="{{ url_for('go_to_cafe') }}"><button class="next-btn">✅ Ya he llegado</button></a>
    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la SÉPTIMA PRUEBA (Parte 2: Acción en la azotea - Diseño Unificado)
TEMPLATE_7_ACTION = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Séptimo Misterio: La Torre</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0, 0, 0, 0.75);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:600px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.2em; font-style: italic; margin-bottom: 30px; }
    .action-list { text-align: left; margin: 30px auto; max-width: 400px; list-style: decimal inside; }
    .action-list li { margin-bottom: 10px; font-size: 1.1em; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; margin-top:20px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; margin-top:20px; }
    @media (max-width:520px){ h1{font-size:32px;} p{font-size:18px;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>☕ El Misterio de la Torre! 🗼</h1>
      
      {% if result == 'ok' %}
        <div class="success">
          <strong>Muy bien! 🎉</strong>
          <p>Has descubierto el siguiente fragmento! (44.3")</p> 
          <p>Disfruta tu café! Guarda bien las coordenadas y a por la siguiente prueba.</p>
          <a href="{{ url_for('puzzle_8') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Siguiente pista ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Número incorrecto 😢</strong>
          <p>El código de la pista no es correcto.</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Lo lograste! Ahora, para obtener la siguiente pista, sigue estos pasos:</p>
        <ol class="action-list">
            <li>Hazte un selfie con tu novio con la torre de mas alta de fondo.</li>
            <li>Entrad y subid a la azotea y pediros un café.</li>
            <li>Una vez estéis tomando algo recibirás la siguiente pista.</li>
        </ol>

        <p class="riddle-text">
        Introduce aquí el número secreto:
        </p>
        
        <form method="POST" action="{{ url_for('submit_7_cafe') }}">
          <input type="text" name="code" placeholder="Escribe el número aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}
    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la octava prueba (Acertijo de la Sagrada Familia)
TEMPLATE_8 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Octavo Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(81, 1, 0, 0.88);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:700px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.5em; font-style: italic; margin-bottom: 30px; border-left: 5px solid #ffeb3b; padding: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ El Gran Paraíso! ✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Maravilloso! 🎉</strong>
          <p>Sabía que lo adivinarías! Dirígete allí guapa.</p>
          <a href="{{ url_for('next_page_9') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Ir al Siguiente Desafío! ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Lugar incorrecto 😢</strong>
          <p></p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Tu siguiente destino te espera si resuelves este acertijo:</p>
        <p class="riddle-text">
        Mi creador, maestro de líneas curvas y adelantado a su época.<br>
        No tengo paredes rectas y mi forma imita a un bosque de piedra donde la luz juega a ser hoja.<br>
        Búscame en el corazón de Barcelona, donde los pilares crecen como árboles gigantes y la fe se aloja.
        </p>
        <form method="POST" action="{{ url_for('submit_8') }}">
          <input type="text" name="code" placeholder="Escribe el nombre del sitio aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Plantilla para la novena prueba (Sagrada Familia - In-situ)
TEMPLATE_9 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Misterio Final</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(8, 0, 80, 0.85);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:700px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#a2e4fa; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.2em; font-style: italic; margin-bottom: 30px; border-left: 5px solid #a2e4fa; padding: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#a2e4fa; color:#080050; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>Ave maría cuando serás mía! </h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Correcto! 🎉</strong>
          <p>Has conseguido la mitad de esta prueba para lograr las coordenadas, pasa ahora a por la segunda parte</p>
          <a href="{{ url_for('next_page_10') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#a2e4fa; color:#080050; font-weight:700; font-size:18px; cursor:pointer;">Segunda parte ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Código incorrecto 😢</strong>
          <p>Vuelve a buscar con atención. </p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Has llegado! Como es un sitio emblemático vamos a dar una vuelta y verlo. Quiero que encuentres la palabra "Gloria" escrita en algún lugar, tranquila que se verá bien, no está en pequeñito. Junto a la palabra "Gloria" encontrarás una palabra muy usada en la religión católica, dimela para pasar a la siguiente pregunta. </p>
        <p class="riddle-text">
        (La palabra es...).
        </p>
        <form method="POST" action="{{ url_for('submit_9') }}">
          <input type="text" name="code" placeholder="Escribe la palabra clave aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''
TEMPLATE_10 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Octavo Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(81, 1, 0, 0.88);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:700px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.5em; font-style: italic; margin-bottom: 30px; border-left: 5px solid #ffeb3b; padding: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨ El Gran Paraíso! ✨</h1>

      {% if result == 'ok' %}
        <div class="success">
          <strong>¡Correcto! 🎉</strong>
          <p>¡Que crack! Este es el siguiente bloque de las coordenadas (N 2°09')</p>
          <a href="{{ url_for('next_page_11') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Ir a la siguiente prueba ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Código incorrecto 😢</strong>
          <p>Intenta de nuevo.</p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>“No es un ángel ni una torre,
pero corona lo más alto del creciente.
Brilla con luz propia y mira al sol naciente.
¿Qué es?”</p>
        <form method="POST" action="{{ url_for('submit_10') }}">
          <input type="text" name="code" placeholder="Soy..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''
TEMPLATE_11 = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Octavo Misterio</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(81, 1, 0, 0.88);  padding:40px; border-radius:20px; color:#fff; width:92%; max-width:200px; box-shadow:0 10px 40px rgba(0,0,0,0.6); text-align:center; position:relative; }
    h1 { margin:0 0 20px 0; font-size:46px; color:#ffeb3b; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); }
    p { margin:12px 0 24px 0; line-height:1.6; font-size:20px; }
    .riddle-text { font-size: 1.5em; font-style: italic; margin-bottom: 30px; border-left: 5px solid #ffeb3b; padding: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; }
    form { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:20px; }
    input[type=text] { flex:1; max-width:400px; padding:14px 16px; border-radius:10px; border:none; font-size:18px; text-align: center; }
    button { padding:14px 20px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:18px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.05); }
    .success { background:#e8f5e9; color:#1b5e20; padding:18px; border-radius:12px; font-size:18px; }
    .error { background:#ffebee; color:#b71c1c; padding:18px; border-radius:12px; font-size:18px; }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      
      <h1>✨La rutilla ✨</h1>
      {% if result == 'ok' %}
        <div class="success">
          <strong>Maravilloso! 🎉</strong>
          <p>Sabía que lo adivinarías! Dirígete allí guapa.</p>
          <a href="{{ url_for('next_page_9') }}"><button style="margin-top:22px; padding:14px 28px; border-radius:10px; border:none; background:#ffeb3b; color:#111; font-weight:700; font-size:18px; cursor:pointer;">Ir al Siguiente Desafío! ➡️</button></a>
        </div>
      {% elif result == 'fail' %}
        <div class="error">
          <strong>Lugar incorrecto 😢</strong>
          <p></p>
        </div>
      {% endif %}

      {% if not result or result == 'fail' %}
        <p>Tu siguiente destino te espera si resuelves este acertijo:</p>
        <p class="riddle-text">
        Mi creador, maestro de líneas curvas y adelantado a su época.<br>
        No tengo paredes rectas y mi forma imita a un bosque de piedra donde la luz juega a ser hoja.<br>
        Búscame en el corazón de Barcelona, donde los pilares crecen como árboles gigantes y la fe se aloja.
        </p>
        <form method="POST" action="{{ url_for('submit_12') }}">
          <input type="text" name="code" placeholder="Escribe el nombre del sitio aquí..." autocomplete="off" required>
          <button type="submit">💌 Enviar</button>
        </form>
      {% endif %}

    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''



# Plantilla para el destino final (recompensa)
FINAL_REWARD_TEMPLATE = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Misión Finalizada! 🎉</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; height:100%; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(50, 150, 50, 0.9);  padding:50px; border-radius:20px; color:#fff; width:92%; max-width:800px; box-shadow:0 10px 50px rgba(0,0,0,0.8); text-align:center; position:relative; display:flex; flex-direction:column; align-items:center; }
    h1 { margin:0 0 20px 0; font-size:70px; color:#ffeb3b; text-shadow: 2px 2px 12px rgba(0,0,0,0.8); }
    p { margin:15px 0 30px 0; line-height:1.7; font-size:2.1em; }
    .coords-finales { font-size:3.2em; color:#ffeb3b; background:rgba(0,0,0,0.5); padding:30px 20px; border-radius:18px; margin:30px 0 40px 0; font-weight:bold; letter-spacing:2px; }
    @media (max-width:900px) { h1{font-size:38px;} .overlay{padding:20px;} .coords-finales{font-size:2em;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      <h1>Misión Finalizada! 🏆</h1>
      
      <p>¡Has resuelto todos los enigmas demostrando tu ingenio! Como regalo extra vas a escoger el restaurante que más te apetezca y vamos a cenar ahora mismo alli, sin miedo al éxito, lo que más se te antoje ahora mismo.</p>
      <p>¡¡¡¡Ve a por tu recompensa, te la mereces!!!</p>
    </div>
  </div>

  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>

  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# ==============================================================================
#                               LÓGICA DE FLASK
# ==============================================================================

@app.route('/')
def index():
    """Página de inicio con la introducción."""
    session.clear()  # Limpia la sesión al inicio
    return render_template_string(INTRO_TEMPLATE, 
                                  bg_image_file=BG_IMAGE_FILE_INTRO, 
                                  music_file=MUSIC_FILE)

# ----------------- PRUEBA 1 -----------------

@app.route('/puzzle_1')
def first_puzzle():
    """Página de la primera prueba (Palabra clave)."""
    intro_text = "Para ir calentando la primera prueba es muy simple, tienes que poner el nombre de la parada de metro mas cercana de cuando nos dimos nuestro primer beso. ¿Cómo se llama?"
    return render_template_string(TEMPLATE_1, 
                                  intro_text=intro_text,
                                  bg_image_file=BG_IMAGE_FILE_1, 
                                  music_file=MUSIC_FILE,
                                  result=None)

@app.route('/submit_1', methods=['POST'])
def submit_1():
    """Ruta para comprobar el código secreto de la Prueba 1."""
    code = request.form['code'].strip().upper()
    intro_text = "Nuestro primer destino fue en un lugar conocido, donde hicimos nuestro primer 'Golfito' ¿Dónde estábamos?"
    
    if code == SECRET_CODE_1.upper():
        return render_template_string(TEMPLATE_1, 
                                      bg_image_file=BG_IMAGE_FILE_1, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    elif code == "PISTA":
        # Pista personalizada para la Prueba 1
        intro_text = "La pista es: El nombre del lugar rima con 'Chira'."
        return render_template_string(TEMPLATE_1, 
                                      intro_text=intro_text,
                                      bg_image_file=BG_IMAGE_FILE_1, 
                                      music_file=MUSIC_FILE, 
                                      result='hint')
    else:
        return render_template_string(TEMPLATE_1, 
                                      intro_text=intro_text,
                                      bg_image_file=BG_IMAGE_FILE_1, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

@app.route('/next_page_2')
def next_page_2():
    """Ruta de transición a la segunda prueba."""
    return redirect(url_for('puzzle_2'))

# ----------------- PRUEBA 2 -----------------

@app.route('/puzzle_2')
def puzzle_2():
    """Página del desafío de código binario."""
    binary_text = "01001011 01000001 01010010 01001111 01010100 01010100 01000101" # KAROTTE en binario
    return render_template_string(TEMPLATE_2, 
                                  binary_text=binary_text,
                                  binary_image_file=BINARY_IMAGE_FILE,
                                  bg_image_file=BG_IMAGE_FILE_2, 
                                  music_file=MUSIC_FILE,
                                  result=None)

@app.route('/submit_2', methods=['POST'])
def submit_2():
    """Ruta para comprobar el código secreto de la Prueba 2."""
    code = request.form['code'].strip().upper()
    binary_text = "01001011 01000001 01010010 01001111 01010100 01010100 01000101"
    
    if code == SECRET_CODE_2.upper():
        return render_template_string(TEMPLATE_2, 
                                      binary_text=binary_text,
                                      binary_image_file=BINARY_IMAGE_FILE,
                                      bg_image_file=BG_IMAGE_FILE_2, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_2, 
                                      binary_text=binary_text,
                                      binary_image_file=BINARY_IMAGE_FILE,
                                      bg_image_file=BG_IMAGE_FILE_2, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

@app.route('/next_page_3')
def next_page_3():
    """Ruta de transición a la tercera prueba."""
    return redirect(url_for('puzzle_3'))

# ----------------- PRUEBA 3 -----------------

@app.route('/puzzle_3')
def puzzle_3():
    """Página del desafío de la prueba 3 (Cálculo numérico)."""
    return render_template_string(TEMPLATE_3, 
                                  bg_image_file=BG_IMAGE_FILE_3, 
                                  music_file=MUSIC_FILE, 
                                  result=None)

@app.route('/submit_3', methods=['POST'])
def submit_3():
    """Ruta para comprobar el código secreto de la Prueba 3."""
    code = request.form['code'].strip().replace(",", ".").upper()
    
    if code == SECRET_CODE_3.replace(",", ".").upper():
        return render_template_string(TEMPLATE_3, 
                                      bg_image_file=BG_IMAGE_FILE_3, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_3, 
                                      bg_image_file=BG_IMAGE_FILE_3, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

@app.route('/start_puzzle_4')
def start_puzzle_4():
    """Ruta de transición a la cuarta prueba (inicia el problema de las jarras)."""
    session['vessels'] = {'v5': 0, 'v3': 0}
    session['puzzle_4_solved'] = False
    return redirect(url_for('puzzle_4'))

# ----------------- PRUEBA 4 -----------------

@app.route('/puzzle_4')
def puzzle_4():
    """Página del desafío de la Sangría (problema de las jarras)."""
    vessels = session.get('vessels', {'v5': 0, 'v3': 0})
    puzzle_solved = session.get('puzzle_4_solved', False)
    message = session.pop('message', None)
    
    return render_template_string(TEMPLATE_4, 
                                  vessels=vessels, 
                                  puzzle_solved=puzzle_solved,
                                  message=message,
                                  bg_image_file=BG_IMAGE_FILE_4,
                                  music_file=MUSIC_FILE)

@app.route('/submit_4', methods=['POST'])
def submit_4():
    """Ruta para manejar las acciones del problema de las jarras."""
    if session.get('puzzle_4_solved', False):
        return redirect(url_for('puzzle_4'))
        
    action = request.form.get('action')
    v5 = session['vessels']['v5']
    v3 = session['vessels']['v3']
    message = None

    if action == 'fill5':
        v5 = 5
    elif action == 'fill3':
        v3 = 3
    elif action == 'empty5':
        v5 = 0
    elif action == 'empty3':
        v3 = 0
    elif action == 'pour5to3':
        transfer = min(v5, 3 - v3)
        v5 -= transfer
        v3 += transfer
    elif action == 'pour3to5':
        transfer = min(v3, 5 - v5)
        v3 -= transfer
        v5 += transfer

    session['vessels']['v5'] = v5
    session['vessels']['v3'] = v3

    if v5 == 4 or v3 == 4:
        session['puzzle_4_solved'] = True
        session['message'] = "Felicidades! Has conseguido los 4 litros exactos!"
    elif message is None:
        session['message'] = f"Movimiento realizado. Jarra 5L: {v5}L, Jarra 3L: {v3}L."

    return redirect(url_for('puzzle_4'))

# ----------------- PASO A LA ACCIÓN (COORDINADAS) -----------------

@app.route('/start_action')
def start_action():
    """Página de presentación de las coordenadas."""
    return render_template_string(ACTION_TEMPLATE, 
                                  bg_image_file=BG_IMAGE_FILE_ACTION, 
                                  music_file=MUSIC_FILE)

# ----------------- PRUEBA 5 -----------------

@app.route('/puzzle_5')
def puzzle_5():
    """Página del desafío de código Morse (Nombre de la calle)."""
    # El código Morse para "PASSEIG DELS TILLERS"
    morse_text = ".--. .- ... ... . .. --. / -.. . .-.. ... / - .. .-.. .-.. . .-. ..." 
    return render_template_string(TEMPLATE_5, 
                                  morse_text=morse_text,
                                  morse_manual_image_file=MORSE_MANUAL_IMAGE_FILE,
                                  bg_image_file=BG_IMAGE_FILE_ACTION, # Usa el fondo de coordenadas
                                  music_file=MUSIC_FILE,
                                  result=None)

@app.route('/submit_5', methods=['POST'])
def submit_5():
    """Ruta para comprobar el código secreto de la Prueba 5."""
    code = request.form['code'].strip().upper()
    morse_text = ".--. .- ... ... . .. --. / -.. . .-.. ... / - .. .-.. .-.. . .-. ..."
    
    # Normaliza el código para comparación (quita espacios, acentos, etc.)
    normalized_secret = SECRET_CODE_5.upper().replace(' ', '').replace('·', '')
    normalized_code = code.replace(' ', '').replace('·', '')

    if normalized_code == normalized_secret:
        return render_template_string(TEMPLATE_5, 
                                      morse_text=morse_text,
                                      morse_manual_image_file=MORSE_MANUAL_IMAGE_FILE,
                                      bg_image_file=BG_IMAGE_FILE_ACTION, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_5, 
                                      morse_text=morse_text,
                                      morse_manual_image_file=MORSE_MANUAL_IMAGE_FILE,
                                      bg_image_file=BG_IMAGE_FILE_ACTION, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

# ----------------- PRUEBA 6 -----------------

@app.route('/puzzle_6')
def puzzle_6():
    """Página del desafío de la prueba 6 (Número de casa)."""
    return render_template_string(TEMPLATE_6, 
                                  bg_image_file=BG_IMAGE_FILE_6, 
                                  music_file=MUSIC_FILE, 
                                  result=None)

@app.route('/submit_6', methods=['POST'])
def submit_6():
    """Ruta para comprobar el código secreto de la Prueba 6."""
    code = request.form['code'].strip().upper()
    
    if code == SECRET_CODE_6.upper():
        return render_template_string(TEMPLATE_6, 
                                      secret_code=SECRET_CODE_6,
                                      bg_image_file=BG_IMAGE_FILE_6, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_6, 
                                      bg_image_file=BG_IMAGE_FILE_6, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

@app.route('/next_page_7')
def next_page_7():
    """Ruta de transición a la prueba 7 (Café/Torre)."""
    return redirect(url_for('puzzle_7'))

# ----------------- PRUEBA 7 -----------------

# Reemplaza la sección 'PRUEBA 7' en tu código Flask con esta:

# ----------------- PRUEBA 7 -----------------

@app.route('/puzzle_7')
def puzzle_7():
    """Primera pantalla de la prueba 7: Ir a la ubicación de la foto."""
    # Asegúrate de que 'cafe_image_file' esté definido en tus variables
    return render_template_string(TEMPLATE_7_IN_SITU, 
                                  bg_image_file=BG_IMAGE_FILE_7, 
                                  cafe_image_file='top.png', # CAMBIA ESTO por tu nombre de archivo real
                                  music_file=MUSIC_FILE)

@app.route('/go_to_cafe')
def go_to_cafe():
    """Ruta para ir a la segunda parte de la prueba 7 (La acción en la azotea)."""
    # Llama a la plantilla de acción/cuestionario
    return render_template_string(TEMPLATE_7_ACTION, 
                                  bg_image_file=BG_IMAGE_FILE_7, 
                                  music_file=MUSIC_FILE,
                                  result=None)

@app.route('/submit_7_cafe', methods=['POST'])
def submit_7_cafe():
    """Ruta para comprobar el código secreto de la Prueba 7 (El número 3)."""
    code = request.form['code'].strip()
    
    # La solución es el número 3, como pediste.
    if code == "3":
        # Almacena el código secreto de la COORDENADA (el fragmento 44)
        secret_code = SECRET_CODE_7 
        return render_template_string(TEMPLATE_7_ACTION, 
                                      secret_code=secret_code,
                                      bg_image_file=BG_IMAGE_FILE_7, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_7_ACTION, 
                                      bg_image_file=BG_IMAGE_FILE_7, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

# El enlace a la siguiente prueba ahora se encuentra en la plantilla 'TEMPLATE_7_ACTION'
# dentro del bloque 'ok', apuntando a 'puzzle_8'.

# ----------------- PRUEBA 8: ACERTIJO SAGRADA FAMILIA -----------------

@app.route('/puzzle_8')
def puzzle_8():
    """Página del acertijo de la Sagrada Familia."""
    return render_template_string(TEMPLATE_8, 
                                  bg_image_file=BG_IMAGE_FILE_8, 
                                  music_file=MUSIC_FILE, 
                                  result=None)

@app.route('/submit_8', methods=['POST'])
def submit_8():
    """Ruta para comprobar el código secreto de la Prueba 8."""
    # Normaliza la entrada y quita espacios
    code = request.form['code'].strip().upper().replace(' ', '')
    
    # Normaliza el código secreto para comparación
    secret = SECRET_CODE_8.upper().replace(' ', '')

    # Acepta también la variante sin espacio
    if code == secret or code == "SAGRADAFAMILIA":
        return render_template_string(TEMPLATE_8, 
                                      bg_image_file=BG_IMAGE_FILE_8, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_8, 
                                      bg_image_file=BG_IMAGE_FILE_8, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

@app.route('/next_page_9')
def next_page_9():
    """Ruta de transición a la prueba 9 (Sagrada Familia - In-situ)."""
    return redirect(url_for('puzzle_9'))


# ----------------- PRUEBA 9: SAGRADA FAMILIA (In-situ) -----------------

@app.route('/puzzle_9')
def puzzle_9():
    """Página del desafío de la Sagrada Familia (in-situ)."""
    return render_template_string(TEMPLATE_9, 
                                  bg_image_file=BG_IMAGE_FILE_9, 
                                  music_file=MUSIC_FILE, 
                                  result=None)

@app.route('/submit_9', methods=['POST'])
def submit_9():
    """Ruta para comprobar el código secreto de la Prueba 9 (palabra final)."""
    code = request.form['code'].strip().upper().replace(' ', '')
    secret = SECRET_CODE_9.upper().replace(' ', '')

    if code == secret:
        # Guarda el fragmento final en la sesión para la página final
        session['final_fragment'] = code[:2]  # O el valor que corresponda
        return render_template_string(TEMPLATE_9, 
                                      secret_code=code[:2], 
                                      bg_image_file=BG_IMAGE_FILE_9, 
                                      music_file=MUSIC_FILE, 
                                      result='ok')
    else:
        return render_template_string(TEMPLATE_9, 
                                      bg_image_file=BG_IMAGE_FILE_9, 
                                      music_file=MUSIC_FILE, 
                                      result='fail')

# Corrige el flujo: después de acertar la 9, el botón debe ir a la 10
@app.route('/next_page_10')
def next_page_10():
  """Ruta de transición a la prueba 10."""
  return redirect(url_for('puzzle_10'))



# ----------------- PRUEBA 10 -----------------


@app.route('/puzzle_10')
def puzzle_10():
  """Página de la prueba 10."""
  return render_template_string(TEMPLATE_10, 
                  bg_image_file=BG_IMAGE_FILE_10, 
                  music_file=MUSIC_FILE, 
                  result=None)


@app.route('/submit_10', methods=['POST'])
def submit_10():
  """Ruta para comprobar el código secreto de la Prueba 10."""
  code = request.form['code'].strip().upper().replace(' ', '')
  secret = SECRET_CODE_10.upper().replace(' ', '')
  if code == secret:
    return render_template_string(TEMPLATE_10, 
                    bg_image_file=BG_IMAGE_FILE_10, 
                    music_file=MUSIC_FILE, 
                    result='ok')
  else:
    return render_template_string(TEMPLATE_10, 
                    bg_image_file=BG_IMAGE_FILE_10, 
                    music_file=MUSIC_FILE, 
                    result='fail')


@app.route('/next_page_11')
def next_page_11():
  """Ruta de transición a la prueba 11."""
  return redirect(url_for('puzzle_11'))

# ----------------- PRUEBA 11: ACERTIJO SAGRADA FAMILIA -----------------





# Plantilla para prueba 11: 7 fotos grandes y texto al lado
TEMPLATE_11_CUSTOM = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>💖 Prueba 11</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; min-height:100vh; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0,0,0,0.85); padding:40px; border-radius:30px; color:#fff; width:98vw; max-width:1800px; min-height:90vh; box-shadow:0 10px 60px rgba(0,0,0,0.7); display:flex; flex-direction:row; gap:40px; align-items:flex-start; justify-content:center; }
    .fotos-col {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-auto-rows: 1fr;
      gap: 28px;
      max-width: 1100px;
      width: 100%;
      align-items: center;
      justify-items: center;
    }
    .fotos-col img {
      width: 100%;
      max-width: 420px;
      max-height: 320px;
      object-fit: cover;
      border-radius: 28px;
      box-shadow:0 4px 24px #0007;
      background:#fff;
      padding:8px;
    }
    .texto-col { max-width:600px; min-width:260px; }
    h1 { margin:0 0 40px 0; font-size:70px; color:#ffeb3b; text-shadow: 2px 2px 12px rgba(0,0,0,0.8); }
    .texto-prueba { font-size:2.1em; margin-bottom:40px; background:rgba(255,255,255,0.08); border-radius:18px; padding:30px; border-left:8px solid #ffeb3b; }
    form { display:flex; gap:18px; align-items:center; justify-content:center; margin-top:30px; }
    input[type=text] { flex:1; max-width:600px; padding:22px 24px; border-radius:16px; border:none; font-size:32px; text-align: center; }
    button { padding:22px 32px; border-radius:16px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:32px; transition:transform 0.2s ease; }
    button:hover { transform:scale(1.07); }
    .success { background:#e8f5e9; color:#1b5e20; padding:28px; border-radius:18px; font-size:28px; }
    .error { background:#ffebee; color:#b71c1c; padding:28px; border-radius:18px; font-size:28px; }
    @media (max-width:1200px) {
      .overlay{flex-direction:column;gap:30px;padding:20px;align-items:center;}
      .fotos-col{grid-template-columns:1fr;max-width:98vw;}
      .fotos-col img{max-width:80vw;max-height:38vw;}
      h1{font-size:38px;}
    }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      <div class="fotos-col">
        {% for foto in fotos %}
          <img src="/static/{{ foto }}" alt="foto {{ loop.index }}">
        {% endfor %}
      </div>
      <div class="texto-col">
        <h1>Prueba 11</h1>
        <div class="texto-prueba">
          {{ texto_prueba }}
        </div>
        {% if result == 'ok' %}
          <div class="success">
            <strong>¡Correcto! 🎉</strong>
            <p>Puedes avanzar a la siguiente prueba.</p>
            <a href="{{ url_for('next_page_12') }}"><button style="margin-top:22px;">Siguiente prueba ➡️</button></a>
          </div>
        {% elif result == 'fail' %}
          <div class="error">
            <strong>Código incorrecto 😢</strong>
            <p>Intenta de nuevo.</p>
          </div>
        {% endif %}
        {% if not result or result == 'fail' %}
          <form method="POST" action="{{ url_for('submit_11') }}">
            <input type="text" name="code" placeholder="Introduce la clave..." autocomplete="off" required>
            <button type="submit">💌 Enviar</button>
          </form>
        {% endif %}
      </div>
    </div>
  </div>
  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>
  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

@app.route('/puzzle_11')
def puzzle_11():
  """Prueba 11: muestra 7 fotos grandes y el texto al lado."""
  fotos = [
    'foto1.jpg',
    'foto2.jpg',
    'foto3.jpg',
    'foto4.jpg',
    'foto5.jpg',
    'foto6.jpg',
    'foto7.jpg',
  ]
  texto_prueba = """
  ¡Bienvenida a la penúltima prueba! Esta prueba consiste en recorrer varios puntos de la ciudad y tendrás que ir sumando los resultados de cada pregunta hasta tener un número final. Es obligatorio quedarse en la moto.
  Las fotos y las preguntas están en su orden correcto, sigue su camino y hazte una foto cuando estés pasando por cada punto.    
  ¿Cuántos balcones de solo 2 agujeros hay?  
  ¿Cuántas fuentes ves?
  ¿Cuántos leones duermen? 
  ¿Cuántos mujeres hay arriba? 
  ¿Cuántos pilares descansan? 
  ¿Qué puerta es?
  ¿Cuántas salidas hay en el circulo?
  """
  return render_template_string(TEMPLATE_11_CUSTOM, 
                  fotos=fotos,
                  texto_prueba=texto_prueba,
                  bg_image_file=BG_IMAGE_FILE_2, 
                  music_file=MUSIC_FILE,
                  result=None)



# Pantalla de enhorabuena tras la prueba 11
TEMPLATE_11_ENHORABUENA = '''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>¡Enhorabuena!</title>
  <style>
    html,body { height:100%; margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .bg { background-image: url('/static/{{ bg_image_file }}'); background-size: cover; background-position: center; min-height:100vh; display:flex; align-items:center; justify-content:center; }
    .overlay { background: rgba(0,0,0,0.85); padding:60px; border-radius:30px; color:#fff; width:92vw; max-width:900px; min-height:60vh; box-shadow:0 10px 60px rgba(0,0,0,0.7); text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; }
    h1 { font-size:70px; color:#ffeb3b; text-shadow: 2px 2px 12px rgba(0,0,0,0.8); margin-bottom:30px; }
    p { font-size:2.1em; margin-bottom:40px; }
    .coords-finales { font-size:3.2em; color:#ffeb3b; background:rgba(0,0,0,0.5); padding:30px 20px; border-radius:18px; margin:30px 0 40px 0; font-weight:bold; letter-spacing:2px; }
    .next-btn { padding:22px 32px; border-radius:16px; border:none; background:#ffeb3b; color:#111; font-weight:700; cursor:pointer; font-size:32px; transition:transform 0.2s ease; }
    .next-btn:hover { transform:scale(1.07); }
    @media (max-width:900px) { h1{font-size:38px;} .overlay{padding:20px;} .coords-finales{font-size:2em;} }
  </style>
</head>
<body>
  <div class="bg">
    <div class="overlay">
      <h1>¡Enhorabuena! 🎉</h1>
      <div class="coords-finales">41°23'44.3"N<br>2°09'08.8"E</div>
      <p>¿Cómo ha ido? Estas son las coordenadas finales. Dirígete al lugar. Cuando estés allí ya sabrás que hacer. Una vez hayas terminado allí dale al botón de seguir.</p>
      <a href="{{ url_for('final_coordinates_page') }}"><button class="next-btn">BOTÓN FINAL</button></a>
    </div>
  </div>
  <audio id="bgMusic" loop>
    <source src="/static/{{ music_file }}" type="audio/mpeg">
    Tu navegador no soporta audio en HTML5.
  </audio>
  <script>
    const music = document.getElementById('bgMusic');
    music.volume = 0.15;
    music.play();
  </script>
</body>
</html>
'''

# Ruta para manejar el submit de la prueba 11
@app.route('/submit_11', methods=['POST'])
def submit_11():
    """Ruta para comprobar el código secreto de la Prueba 11."""
    code = request.form['code'].strip().upper().replace(' ', '')
    secret = SECRET_CODE_11.upper().replace(' ', '')
    fotos = [
        'foto1.jpg',
        'foto2.jpg',
        'foto3.jpg',
        'foto4.jpg',
        'foto5.jpg',
        'foto6.jpg',
        'foto7.jpg',
    ]
    texto_prueba = """
    ¡Bienvenida a la penúltima prueba! Esta prueba consiste en recorrer varios puntos de la ciudad y tendrás que ir sumando los resultados de cada pregunta hasta tener un número final. Es obligatorio quedarse en la moto.
    Las fotos y las preguntas están en su orden correcto, sigue su camino.    
    ¿Cuántos pisos hay?  
    ¿Cuántos caballos estan?
    ¿Cuántos leones duermen? 
    ¿Cuántos mujeres hay arriba? 
    ¿Cuántos pilares descansan? 
    ¿Qué puerta es?
    ¿Cuántas salidas hay en el circulo?
    """
    if code == secret:
        # Si la respuesta es correcta, muestra pantalla de enhorabuena antes del destino final
        return render_template_string(TEMPLATE_11_ENHORABUENA,
                                      bg_image_file=BG_IMAGE_FILE_2,
                                      music_file=MUSIC_FILE)
    else:
        # Si es incorrecto, muestra el error en la misma pantalla
        return render_template_string(TEMPLATE_11_CUSTOM,
                                      fotos=fotos,
                                      texto_prueba=texto_prueba,
                                      bg_image_file=BG_IMAGE_FILE_2,
                                      music_file=MUSIC_FILE,
                                      result='fail')






@app.route('/final_coordinates_page')
def final_coordinates_page():
    """Página final de revelación de la coordenada completa."""
    # Los fragmentos se obtienen de las pruebas 6, 7 y 9
    
    # Fragmento A (ejemplo: '44.XX'): Podría ser el fragmento que se obtiene en la prueba 9
    final_code_a = session.get('final_fragment', '??') 
    
    # Fragmento B (ejemplo: '08.XX'): Podría ser el fragmento que se obtiene en la prueba 7
    final_code_b = SECRET_CODE_7.upper() + SECRET_CODE_6.upper() # Usando códigos de ejemplo
    
    # Nota: Debes ajustar la lógica de qué fragmento corresponde a qué código.
    # Usaré los que definiste:
    # Bloque 1 (Prueba 6): 41°XX'44.?"? -> XX = SECRET_CODE_6 = "23"
    # Bloque 2 (Prueba 7): 2°09'08.XX"? -> XX = SECRET_CODE_7 = "3"
    # Bloque 3 (Prueba 9): Coordenada final (Usaremos las dos primeras letras de BARCELONA)
    
    coord_minutos = SECRET_CODE_6 # El 23
    coord_segundos_b = SECRET_CODE_7 # El 3
    coord_segundos_a = session.get('final_fragment', 'BA') # Usando 'BA' como ejemplo de 'BARCELONA'

    # Coordenadas finales a mostrar (Ejemplo: 41°23'44.155"N 2°09'08.232"E)
    
    # Simplemente rellenamos los huecos con todos los códigos.
    # Coordenada 1: 41°[C6]'44.[C7][C9a] -> 41°23'44.3B
    # Coordenada 2: 2°09'08.[C9b][C9c] -> 2°09'08.AR

    # Fragmentos a mostrar en la plantilla
    final_coord_lat = f"{SECRET_CODE_6}'44.{SECRET_CODE_7}{SECRET_CODE_9[0]}" # 23'44.3B
    final_coord_lon = f"09'08.{SECRET_CODE_9[1]}{SECRET_CODE_9[2]}" # 09'08.AR
    
    final_message = f"41°{final_coord_lat} 2°{final_coord_lon}"

    return render_template_string(FINAL_REWARD_TEMPLATE,
                                  final_code_a=final_coord_lat,
                                  final_code_b=final_coord_lon,
                                  music_file=MUSIC_FILE,
                                  bg_image_file=BG_IMAGE_FILE_12)


# --- INICIO DE LA APP ---
if __name__ == '__main__':
    # Define la carpeta static si no existe (aunque Flask la crea por defecto)
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Asegúrate de que las imágenes necesarias existan, o el programa fallará
    # Esto es solo una verificación de archivos críticos.
    required_files = [BG_IMAGE_FILE_INTRO, BG_IMAGE_FILE_1, BG_IMAGE_FILE_2, BG_IMAGE_FILE_3, BG_IMAGE_FILE_4, BG_IMAGE_FILE_ACTION, BG_IMAGE_FILE_6, BG_IMAGE_FILE_7, BG_IMAGE_FILE_8, BG_IMAGE_FILE_9, BINARY_IMAGE_FILE, MORSE_MANUAL_IMAGE_FILE, MUSIC_FILE]
    
    missing_files = [f for f in required_files if not os.path.exists(os.path.join('static', f))]
    
    if missing_files:
        print("ADVERTENCIA CRÍTICA! Faltan archivos de imagen/música necesarios en la carpeta 'static/':")
        for f in missing_files:
            print(f"- {f}")
        print("Por favor, asegúrate de que todos los archivos listados en la CONFIGURACIÓN existen en la carpeta 'static/' antes de ejecutar.")
        # Se puede forzar a salir aquí si se desea, pero lo dejaremos advertir y ejecutar.
    
    app.run(debug=True)