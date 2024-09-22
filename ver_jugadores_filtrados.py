from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
conn = sqlite3.connect('jugadores.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Función para verificar si el equipo es Liverpool y aplicar un estilo especial de fondo rojo
def aplicar_estilo_liverpool(team_name, team_imageUrl):
    if team_name.lower() == 'liverpool':
        return 'https://oneftbl-cms.imgix.net/https%3A%2F%2Fimages.onefootball.com%2Ficons%2Fteams%2F164%2F18.png?auto=format%2Ccompress&crop=faces&dpr=2&fit=crop&h=0&q=25&w=128&s=84ded2da372fccd6155ac95ab4679cc5' 
    elif team_name.lower() == 'notting. forest':
        return 'https://oneftbl-cms.imgix.net/https%3A%2F%2Fimages.onefootball.com%2Ficons%2Fteams%2F164%2F577.png?auto=format%2Ccompress&crop=faces&dpr=2&fit=crop&h=0&q=25&w=128&s=12eaab8869aa89822e07b67fb388c007'
    return team_imageUrl  # Si no es Liverpool, no aplicar ningún estilo

def aplicar_estilo_nombre(team_name):
    if team_name.lower() == 'man utd':
        return 'Manchester United'
    elif team_name.lower() == 'spurs':
        return 'Tottenham Hotspur'
    elif team_name.lower() == 'notting. forest':
        return 'Nottingham Forest'
    elif team_name.lower() == 'newcastle utd':
        return 'Newcastle United'
    return team_name

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
            # Aplicar estilo rojo si el equipo es Liverpool
            estilo_liverpool = aplicar_estilo_liverpool(equipo['team_label'],equipo['team_imageUrl'])
            estilo_nombre = aplicar_estilo_nombre(equipo['team_label'])

            equipos_html += f"""
            <div style="flex: 1 0 25%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid #ccc; padding: 10px;">
                    <p>ID del Equipo: {equipo['team_id']}<br>
                    Nombre del Equipo: {estilo_nombre}<br>
                    Jugadores: {equipo['total_jugadores']}</p>
                    <!-- Contenedor del escudo con posible fondo rojo -->
                    <div style="">
                        <img src="{estilo_liverpool}" style="width: 50px; height: 50px; vertical-align: middle;">
                    </div><br>
                    <!-- Botón de Ver Plantel -->
                    <a href="/equipo/{equipo['team_id']}" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px; font-family: Arial, sans-serif;">Ver plantel</a>
                </div>
            </div>
            """  # Cada equipo ocupará 25% del ancho.

        # Agregar cuadros vacíos si es necesario
        total_equipos = len(equipos)
        cuadros_vacios_a_agregar = (4 - total_equipos % 4) % 4  # Cálculo para rellenar la última fila

        for _ in range(cuadros_vacios_a_agregar):
            equipos_html += """
            <div style="flex: 1 0 25%; box-sizing: border-box; padding: 10px;">
                <div style="border: 1px solid transparent; padding: 10px; height: 100px;">
                    <!-- Cuadro vacío -->
                </div>
            </div>
            """

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
            position_id_formateado = str(jugador['position_id']).zfill(2)  # Mostrar el ID de posición con dos dígitos
            equipo_id_formateado = str(jugador['team_id']).zfill(2)     # Ejemplo para el ID del equipo

            # Obtener el estilo especial si es Liverpool
            estilo_liverpool = aplicar_estilo_liverpool(jugador['team_label'],jugador['team_imageUrl'])  # jugador[7] es el nombre del equipo
            estilo_nombre = aplicar_estilo_nombre(jugador['team_label'])

            jugadores_html += f"""
            <div style="flex: 1 0 30%; box-sizing: border-box; padding: 10px;">
                <div style="display: flex; border: 1px solid #ccc; padding: 10px;">
                    <!-- Primera columna con texto, bandera y escudo -->
                    <div style="flex: 1;">
                        <p>ID: {jugador['id']}<br>
                        Overall Rating: {jugador['overallRating']}<br>
                        Nombre: {jugador['name']}<br>
                        Nacionalidad ID: {str(jugador['nationality_id']).zfill(2)}  |  Bandera: {jugador['nationality_label']}<br>
                        Equipo ID: {equipo_id_formateado}  |  Equipo: {estilo_nombre}<br>
                        Posición ID: {position_id_formateado}  |  Posición: {jugador['position_shortLabel']}</p>

                        <div style="display: inline-flex; align-items: center;">
                            <span style="margin-right: 5px;">Nacionalidad:</span>
                            <img src="{jugador['nationality_imageUrl']}" style="width: 20px; height: 20px; vertical-align: middle;">
                        </div>
                        <br>
                        <div style="display: inline-flex; align-items: center;">
                            <span style="margin-right: 5px;">Escudo del equipo:</span>
                            <!-- Contenedor del escudo con posible fondo rojo -->
                            <div style="">
                                <img src="{estilo_liverpool}" style="width: 30px; height: 30px; vertical-align: middle;">
                            </div>
                        </div>
                    </div>

                    <!-- Segunda columna con la imagen del jugador -->
                    <div style="flex: 0 0 120px; display: flex; justify-content: center; align-items: center;">
                        <img src="{jugador['avatarUrl']}" style="width: 100px; height: 100px;">
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


def paginaEstilo(titulo, body):
    html_template = f"""
    <html>
    <head>
        <title>{titulo}</title>
        <style>
            /* Estilos predeterminados */
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
            }}
            .equipo-container {{
                border: 1px solid #ccc;
                padding: 10px;
                margin: 10px;
            }}
            .dark-mode {{
                background-color: #121212;
                color: #e0e0e0;
            }}
            .dark-mode .equipo-container {{
                border-color: #444;
            }}
            .toggle-button {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>

        <button class="toggle-button" onclick="toggleMode()">Modo Oscuro</button>

        {body}

        <script>
            // Función para alternar entre modo claro y oscuro
            function toggleMode() {{
                const body = document.body;
                body.classList.toggle('dark-mode');

                // Cambiar el texto del botón dependiendo del modo
                const button = document.querySelector('.toggle-button');
                if (body.classList.contains('dark-mode')) {{
                    button.textContent = 'Modo Claro';
                }} else {{
                    button.textContent = 'Modo Oscuro';
                }}

                // Guardar el estado en localStorage
                localStorage.setItem('dark-mode', body.classList.contains('dark-mode'));
            }}

            // Verificar el estado al cargar la página
            window.onload = function() {{
                const darkMode = localStorage.getItem('dark-mode') === 'true';
                if (darkMode) {{
                    document.body.classList.add('dark-mode');
                    document.querySelector('.toggle-button').textContent = 'Modo Claro';
                }}
            }};
        </script>
    </body>
    </html>
    """
    return html_template

# Ruta para mostrar la lista de equipos
@app.route('/')

def mostrar_equipos():
    equipos_html = generar_html_equipos()
    html = paginaEstilo(titulo="Lista de Equipos", body=equipos_html)
    return render_template_string(html)



# Ruta para mostrar los jugadores de un equipo específico
@app.route('/equipo/<team_id>')
def mostrar_jugadores(team_id):
    jugadores_html = generar_html_jugadores(team_id)
    html = paginaEstilo(titulo="Plantel del Equipo", body=f"""
        <!-- Botón de regreso con flecha curva -->
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #6c757d; color: white; text-decoration: none; border-radius: 5px; font-family: Arial, sans-serif;">↩ Volver a la lista de equipos</a>
        <br><br>
        {jugadores_html}
    """)
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
