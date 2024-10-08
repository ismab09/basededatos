from flask import Flask, request, session, render_template_string
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar sesiones

# Función para obtener un país aleatorio desde la tabla 'players'
def obtener_pais_aleatorio():
    conn = sqlite3.connect('jugadores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT team_country FROM players")
    paises = cursor.fetchall()
    conn.close()

    if paises:  # Verificar si se obtuvieron países
        return random.choice(paises)[0]
    return None  # Devolver None si no hay países

# Función para obtener un número limitado de equipos de un país específico
def obtener_equipos(pais):
    conn = sqlite3.connect('jugadores.db')
    cursor = conn.cursor()
    cursor.execute("SELECT team_label FROM players WHERE team_country = ?", (pais,))
    equipos = cursor.fetchall()
    conn.close()
    return [equipo[0] for equipo in equipos][:20]  # Limitar a 20 equipos

# Normalizar nombres de equipos para comparación
def normalizar_nombre(nombre):
    return nombre.strip().lower().replace('cf', '').replace('club', '').replace(' ', '')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'contador' not in session:
        session['contador'] = 1  # Iniciar el contador en 1

    if request.method == 'POST':
        pais = request.form.get('pais')
        equipos = obtener_equipos(pais)
        respuesta = request.form.get('equipo').strip().lower()  # Normalizar a minúsculas

        # Verificar si la respuesta es válida (parcial o completa)
        encontrado = any(normalizar_nombre(respuesta) in normalizar_nombre(equipo) for equipo in equipos)

        # Actualizar la lista de respuestas
        if encontrado:
            session['respuestas'].append(respuesta.capitalize())
            mensaje = f'¡Correcto! {respuesta.capitalize()} pertenece a {pais}'
        else:
            mensaje = f'{respuesta.capitalize()} no pertenece a {pais}. Intenta de nuevo.'

        session['contador'] += 1  # Incrementar el contador en cada intento

        # Plantilla HTML en una cadena
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Equipos de Fútbol</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #2c3e50;
                        color: white;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        display: flex;
                        justify-content: space-between;
                        max-width: 800px;
                        margin: auto;
                        padding: 20px;
                        background-color: #34495e;
                        border-radius: 10px;
                    }
                    .list {
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                    }
                    .list .team-box {
                        width: 48%; /* Cada box ocupará cerca del 50% */
                        padding: 10px;
                        background-color: #1abc9c;
                        margin-bottom: 10px;
                        border-radius: 5px;
                        text-align: left;
                    }
                    .list .team-number {
                        display: inline-block;
                        width: 15%;
                        text-align: center;
                    }
                    .form-container {
                        flex: 1;
                        text-align: center;
                    }
                    input[type="text"] {
                        padding: 10px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                        margin-top: 10px;
                        width: 80%;
                    }
                    button {
                        padding: 10px 20px;
                        background-color: #3498db;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #2980b9;
                    }
                </style>
            </head>
            <body>
                <h1>¿Qué equipos pertenecen a {{ liga }}?</h1>
                <div class="container">
                    <div class="list">
                        <div class="team-boxes">
                            {% for i in range(10) %}
                                <div class="team-box">
                                    <span class="team-number">{{ i + 1 }}</span> 
                                    {% if i < session.respuestas|length %}
                                        {{ session.respuestas[i] }}
                                    {% else %}
                                        ________
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                        <div class="team-boxes">
                            {% for i in range(10, 20) %}
                                <div class="team-box">
                                    <span class="team-number">{{ i + 1 }}</span> 
                                    {% if i < session.respuestas|length %}
                                        {{ session.respuestas[i] }}
                                    {% else %}
                                        ________
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="form-container">
                        <p>{{ mensaje }}</p>
                        <form method="post">
                            <label for="equipo">Ingresa un equipo:</label>
                            <input type="text" id="equipo" name="equipo">
                            <input type="hidden" name="pais" value="{{ pais }}">
                            <button type="submit">Enviar</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
        ''', liga=session['liga'], pais=pais, contador=session['contador'], mensaje=mensaje)

    pais_aleatorio = obtener_pais_aleatorio()

    if pais_aleatorio:
        if pais_aleatorio.lower() == 'inglaterra':
            liga = 'Premier League'
        elif pais_aleatorio.lower() == 'españa':
            liga = 'LaLiga'
        else:
            liga = pais_aleatorio

        session['liga'] = liga
        session['contador'] = 1  # Reiniciar el contador al comenzar nuevo juego
        session['respuestas'] = []  # Reiniciar la lista de respuestas

        # Obtener el número total de equipos para mostrar los espacios en blanco
        equipos = obtener_equipos(pais_aleatorio)

        # Plantilla HTML en una cadena
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Equipos de Fútbol</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #2c3e50;
                        color: white;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        display: flex;
                        justify-content: space-between;
                        max-width: 800px;
                        margin: auto;
                        padding: 20px;
                        background-color: #34495e;
                        border-radius: 10px;
                    }
                    .list {
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                    }
                    .list .team-box {
                        width: 48%; /* Cada box ocupará cerca del 50% */
                        padding: 10px;
                        background-color: #1abc9c;
                        margin-bottom: 10px;
                        border-radius: 5px;
                        text-align: left;
                    }
                    .list .team-number {
                        display: inline-block;
                        width: 15%;
                        text-align: center;
                    }
                    .form-container {
                        flex: 1;
                        text-align: center;
                    }
                    input[type="text"] {
                        padding: 10px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                        margin-top: 10px;
                        width: 80%;
                    }
                    button {
                        padding: 10px 20px;
                        background-color: #3498db;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #2980b9;
                    }
                </style>
            </head>
            <body>
                <h1>¿Qué equipos pertenecen a {{ liga }}?</h1>
                <div class="container">
                    <div class="list">
                        <div class="team-boxes">
                            {% for j in range(20) %}
                                <div class="team-box">
                                    <span class="team-number">{{ j + 1 }}</span>
                                    ________
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="form-container">
                        <form method="post">
                            <label for="equipo">Ingresa un equipo:</label>
                            <input type="text" id="equipo" name="equipo">
                            <input type="hidden" name="pais" value="{{ pais }}">
                            <button type="submit">Enviar</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
        ''', liga=liga, pais=pais_aleatorio)

if __name__ == '__main__':
    app.run(debug=True)
