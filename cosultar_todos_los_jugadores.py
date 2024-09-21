from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
conn = sqlite3.connect('jugadores.db', check_same_thread=False)
cursor = conn.cursor()

# Función para generar la plantilla HTML con los jugadores
def generar_html_jugadores():
    # Ejecutar una consulta SQL para seleccionar todos los jugadores
    cursor.execute('SELECT * FROM players')

    # Obtener todos los resultados
    jugadores = cursor.fetchall()

    # Verificar si hay jugadores en la base de datos
    if jugadores:
        jugadores_html = ""
        for jugador in jugadores:
            jugadores_html += f"""
            <div style="border-bottom: 1px solid #ccc; padding: 10px; display: flex;">
                <!-- Primera columna con texto, bandera y escudo -->
                <div style="flex: 1;">
                    <p>ID: {jugador[0]}<br>
                    Overall Rating: {jugador[1]}<br>
                    Nombre: {jugador[2]}<br>
                    Nacionalidad ID: {jugador[3]}  |  Nacionalidad: {jugador[4]}<br>
                    Equipo ID: {jugador[6]}  |  Equipo: {jugador[7]}<br>
                    Posición ID: {jugador[9]}  |  Posición: {jugador[10]}</p>

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
            <hr>
            """
        return jugadores_html
    else:
        return "<p>No hay jugadores en la base de datos.</p>"


@app.route('/')
def mostrar_jugadores():
    jugadores_html = generar_html_jugadores()
    html_template = f"""
    <html>
    <head>
        <title>Jugadores</title>
    </head>
    <body>
        <h1>Lista de Jugadores</h1>
        {jugadores_html}
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
