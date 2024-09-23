from flask import Flask, render_template_string, request
import sqlite3
from equipos_y_jugadores import generar_html_equipos, generar_html_jugadores, paginaEstilo
from buscador import generar_html_buscador, buscar  # Importa las funciones del buscador

app = Flask(__name__)

# Conexión a la base de datos
conn = sqlite3.connect('jugadores.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Diccionario con banderas de los países
flags = {
    "Inglaterra": "https://upload.wikimedia.org/wikipedia/en/b/be/Flag_of_England.svg",
    "Espana": "https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg"
}

# Función para generar la plantilla HTML con los países
def generar_html_paises():
    cursor.execute('SELECT DISTINCT team_country FROM players WHERE team_country IS NOT NULL')
    paises = cursor.fetchall()

    if paises:
        paises_html = """
        <h1>Selecciona un país</h1>
        <div style="display: flex; flex-wrap: wrap;">
        """ 

        for pais in paises:
            pais_nombre = pais['team_country'].capitalize()
            bandera = flags.get(pais_nombre, "")

            paises_html += f"""
            <div style="flex: 1 0 20%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid #ccc; padding: 10px; text-align: center;">
                    <p>{pais_nombre}</p>
                    <img src="{bandera}" style="width: 50px; height: 30px; vertical-align: middle;">
                    <br><br>
                    <a href="/equipos/{pais_nombre}" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px; font-family: Arial, sans-serif;">Ver equipos</a>
                </div>
            </div>
            """

        total_paises = len(paises)
        cuadros_vacios_a_agregar = (5 - total_paises % 5) % 5

        for _ in range(cuadros_vacios_a_agregar):
            paises_html += """
            <div style="flex: 1 0 20%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid transparent; padding: 10px; height: 100px;">
                </div>
            </div>
            """

        paises_html += "</div>"
        return paises_html
    else:
        return "<p>No hay países disponibles.</p>"

# Ruta para mostrar la lista de países
@app.route('/')
def mostrar_paises():
    paises_html = generar_html_paises() + generar_html_buscador()  # Agregar el buscador
    html = paginaEstilo(titulo="Lista de Países", body=paises_html)
    return render_template_string(html)

# Ruta para mostrar la lista de equipos de un país
@app.route('/equipos/<team_country>')
def mostrar_equipos_pais(team_country):
    equipos_html = generar_html_equipos(team_country)
    html = paginaEstilo(titulo=f'Equipos de {team_country}', body=f"""
    <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #6c757d; color: white; text-decoration: none; border-radius: 5px; font-family: Arial, sans-serif;">↩ Volver a la lista de países</a>
    <br><br>
    {equipos_html}
    """)
    return render_template_string(html)

# Ruta para mostrar los jugadores de un equipo
@app.route('/equipo/<team_id>')
def mostrar_jugadores_equipo(team_id):
    team_country = cursor.execute('SELECT DISTINCT team_country FROM players WHERE team_id = ?', (team_id,)).fetchone()[0]
    jugadores_html = generar_html_jugadores(team_id)

    html = paginaEstilo(titulo="Plantel del Equipo", body=f"""
        <a href="/equipos/{team_country}" style="display: inline-block; padding: 10px 20px; background-color: #6c757d; color: white; text-decoration: none; border-radius: 5px; font-family: Arial, sans-serif;">↩ Volver a la lista de equipos</a>
        <br><br>
        {jugadores_html}
    """)
    return render_template_string(html)

# Ruta para el buscador
@app.route('/buscador', methods=['GET', 'POST'])
def buscar_jugadores():
    query = request.form['query']
    resultados = buscar(query)  # Llama a la función buscar en buscador.py
    html = paginaEstilo(titulo="Resultados de la búsqueda", body=resultados)
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
