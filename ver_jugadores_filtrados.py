from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
conn = sqlite3.connect('jugadores.db', check_same_thread=False)
cursor = conn.cursor()

# Función para generar la plantilla HTML con los equipos
def generar_html_equipos():
    # Ejecutar una consulta SQL para contar cuántos jugadores hay por equipo
    cursor.execute('SELECT team_id, team_label, team_imageUrl, COUNT(*) as total_jugadores FROM players GROUP BY team_id, team_label, team_imageUrl')
    equipos = cursor.fetchall()

    # Verificar si hay equipos en la base de datos
    if equipos:
        equipos_html = """
        <h1>Selecciona un equipo</h1>
        <div style="display: flex; flex-wrap: wrap;">
        """  # Contenedor para mostrar los equipos

        for equipo in equipos:
            equipos_html += f"""
            <div style="flex: 1 0 25%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid #ccc; padding: 10px;">
                    <p>ID del Equipo: {equipo[0]}<br>
                    Nombre del Equipo: {equipo[1]}<br>
                    Jugadores: {equipo[3]}</p>
                    <img src="{equipo[2]}" style="width: 50px; height: 50px; vertical-align: middle;"><br>

                    <!-- Enlace para seleccionar el equipo y ver el plantel -->
                    <a href="/equipo/{equipo[0]}" style="text-decoration: none; color: blue;">Ver plantel</a>
                </div>
            </div>
            """  # Cada equipo ocupará 20% del ancho.

        equipos_html += "</div>"  # Cerrar el contenedor de los equipos.
        return equipos_html
    else:
        return "<p>No hay equipos en la base de datos.</p>"

# Función para generar la plantilla HTML con los jugadores de un equipo
def generar_html_jugadores(team_id):
    # Ejecutar una consulta SQL para seleccionar los jugadores de un equipo específico ordenados por posición y GRL
    cursor.execute('SELECT * FROM players WHERE team_id = ? ORDER BY position_id + 0, overallRating DESC', (team_id,))
    jugadores = cursor.fetchall()

    # Verificar si hay jugadores en el equipo
    if jugadores:
        jugadores_html = """
        <h1>Plantel del equipo</h1>
        <div style="display: flex; flex-wrap: wrap;">
        """  # Contenedor principal flex para colocar tres jugadores por fila.

        # Total de jugadores y cálculo de cuántos "vacíos" hay que agregar
        total_jugadores = len(jugadores)
        vacios_a_agregar = (3 - total_jugadores % 3) % 3  # Cálculo para rellenar la última fila

        # Generar el HTML para cada jugador
        for jugador in jugadores:
            # Aplicar zfill solo para mostrar, no para ordenar
            position_id_formateado = str(jugador[9]).zfill(2)  # Mostrar el ID de posición con dos dígitos
            equipo_id_formateado = str(jugador[6]).zfill(2)     # Ejemplo para el ID del equipo

            jugadores_html += f"""
            <div style="flex: 1 0 30%; box-sizing: border-box; padding: 10px;">
                <div style="display: flex; border: 1px solid #ccc; padding: 10px;">
                    <!-- Primera columna con texto, bandera y escudo -->
                    <div style="flex: 1;">
                        <p>ID: {jugador[0]}<br>
                        Overall Rating: {jugador[1]}<br>
                        Nombre: {jugador[2]}<br>
                        Nacionalidad ID: {str(jugador[3]).zfill(2)}  |  Bandera: {jugador[4]}<br>
                        Equipo ID: {equipo_id_formateado}  |  Equipo: {jugador[7]}<br>
                        Posición ID: {position_id_formateado}  |  Posición: {jugador[10]}</p>

                        <div style="display: inline-flex; align-items: center;">
                            <span style="margin-right: 5px;">Nacionalidad:</span>
                            <img src="{jugador[5]}" style="width: 20px; height: 20px; vertical-align: middle;">
                        </div>
                        <br>
                        <div style="display: inline-flex; align-items: center;">
                            <span style="margin-right: 5px;">Escudo del equipo:</span>
                            <img src="{jugador[8]}" style="width: 30px; height: 30px; vertical-align: middle;">
                        </div>
                    </div>

                    <!-- Segunda columna con la imagen del jugador -->
                    <div style="flex: 0 0 120px; display: flex; justify-content: center; align-items: center;">
                        <img src="{jugador[11]}" style="width: 100px; height: 100px;">
                    </div>
                </div>
            </div>
            """  # Cada jugador ocupará 30% del ancho, y dentro se organizan en dos columnas.

        # Agregar los "cuadrados vacíos" si es necesario
        for _ in range(vacios_a_agregar):
            jugadores_html += """
            <div style="flex: 1 0 30%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid transparent; padding: 10px; height: 200px;">
                    <!-- Cuadro vacío -->
                </div>
            </div>
            """

        jugadores_html += "</div>"  # Cerramos el contenedor principal flex.
        return jugadores_html
    else:
        return "<p>No hay jugadores en este equipo.</p>"

# Ruta para mostrar la lista de equipos
@app.route('/')
def mostrar_equipos():
    equipos_html = generar_html_equipos()
    html_template = f"""
    <html>
    <head>
        <title>Equipos</title>
    </head>
    <body>
        {equipos_html}
    </body>
    </html>
    """
    return render_template_string(html_template)

# Ruta para mostrar los jugadores de un equipo específico
@app.route('/equipo/<team_id>')
def mostrar_jugadores(team_id):
    jugadores_html = generar_html_jugadores(team_id)
    html_template = f"""
    <html>
    <head>
        <title>Plantel</title>
    </head>
    <body>
        {jugadores_html}
        <br>
        <a href="/" style="text-decoration: none; color: blue;">Volver a la lista de equipos</a>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
