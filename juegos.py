from flask import Flask, render_template_string, request
import sqlite3
import equipos_liga  # Asegúrate de que este archivo tiene las funciones necesarias

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar sesiones
# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('jugadores.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    juegos = ["Juego de Equipos de Liga"]  # Aquí puedes agregar más juegos si lo deseas
    return render_template_string(generar_menu(juegos))

def generar_menu(juegos):
    if not juegos:  # Verifica si 'juegos' es None o una lista vacía
        return "No hay juegos disponibles"

    html = "<h1>Selecciona un juego</h1>\n"
    html += '<div style="display: flex; flex-wrap: wrap;">\n'

    for juego in juegos:
        # Agrega un enlace al juego
        html += f'<div style="margin: 10px;"><a href="/{juego.lower().replace(" ", "_")}">{juego}</a></div>\n'

    html += "</div>"
    return html

@app.route('/juego_de_equipos_de_liga', methods=["GET", "POST"])
def juego_de_equipos_de_liga():
    if request.method == "POST":
        # Aquí va la lógica del juego
        # Por ejemplo, llamar a una función en equipos_liga.py
        return equipos_liga.jugar()  # Asegúrate de que esta función exista en equipos_liga.py
    return equipos_liga.index()  # Asegúrate de que esta función exista y retorne el HTML del juego

if __name__ == '__main__':
    app.run(debug=True)
