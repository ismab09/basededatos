from flask import Flask, render_template_string, request
import sqlite3

def abrir_base_datos():
    conn = sqlite3.connect('jugadores.db')
    return conn

def buscar_en_base_datos(query):
    conn = abrir_base_datos()
    cursor = conn.cursor()

    # Buscar en jugadores y equipos, incluyendo team_country
    cursor.execute("""
        SELECT team_label, name, team_country 
        FROM players 
        WHERE name LIKE ? OR team_label LIKE ?
    """, (f'%{query}%', f'%{query}%'))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def generar_html_buscador():
    return '''
    <form method="POST" action="/buscador" style="display: block; margin: 10px 0;">
        <input type="text" name="query" placeholder="Buscar..." required>
        <button type="submit">Buscar</button>
    </form>
    '''

def buscar(query):
    resultados = buscar_en_base_datos(query)
    html = '''
    <h1>Resultados de la búsqueda</h1>
    <ul>
    '''

    for resultado in resultados:
        team_label = resultado[0]
        player_name = resultado[1]
        team_country = resultado[2]  # Obtiene el país directamente de la consulta

        html += f'<li>Equipo: {team_label} ({team_country}), Jugador: {player_name}</li>'

    html += '''
    </ul>
    <a href="/">Volver a la página principal</a>
    '''
    return html

# Si deseas que este archivo se ejecute de forma independiente (opcional)
if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True)
