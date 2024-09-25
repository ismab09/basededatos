import json
import sqlite3

# Conexión a la base de datos (crea la base de datos si no existe)
conn = sqlite3.connect('jugadores.db')
cursor = conn.cursor()

# Crear tabla si no existe (agregamos el campo avatarUrl)
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    overallRating INTEGER,
    name TEXT,
    nationality_id INTEGER,
    nationality_label TEXT,
    nationality_imageUrl TEXT,
    team_id INTEGER,
    team_label TEXT,
    team_imageUrl TEXT,
    position_id TEXT,
    position_shortLabel TEXT,
    avatarUrl TEXT
)
''')

# Función para insertar un jugador en la base de datos
def insertar_jugador(jugador):
    # Preparar los datos
    player_id = jugador['id']
    overall_rating = jugador['overallRating']

    # Verificar si tiene commonName, si no, usar firstName y lastName
    name = jugador['commonName'] if jugador['commonName'] else f"{jugador['firstName']} {jugador['lastName']}"

    # Nacionalidad
    nationality_id = jugador['nationality']['id']
    nationality_label = jugador['nationality']['label']
    nationality_imageUrl = jugador['nationality']['imageUrl']

    # Equipo
    team_id = jugador['team']['id']
    team_label = jugador['team']['label']
    team_imageUrl = jugador['team']['imageUrl']

    # Posición
    position_id = jugador['position']['id']
    position_shortLabel = jugador['position']['shortLabel']

    # Avatar URL
    avatar_url = jugador.get('avatarUrl', None)  # Usamos .get() para evitar errores si el campo no existe

    # Insertar en la base de datos
    cursor.execute('''
    INSERT INTO players (id, overallRating, name, nationality_id, nationality_label, nationality_imageUrl,
                         team_id, team_label, team_imageUrl, position_id, position_shortLabel, avatarUrl)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (player_id, overall_rating, name, nationality_id, nationality_label, nationality_imageUrl,
          team_id, team_label, team_imageUrl, position_id, position_shortLabel, avatar_url))

    # Guardar los cambios
    conn.commit()

# Función para leer un archivo JSON con múltiples jugadores e insertarlos en la base de datos
def insertar_jugadores_desde_json(ruta_json):
    # Leer el archivo JSON
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

        # Para cada jugador en el JSON, lo insertamos en la base de datos
        for jugador in datos['items']:
            insertar_jugador(jugador)

# Ejemplo de uso: lectura de un archivo JSON e inserción de jugadores
ruta_json = 'equipos/España/461_valenciacf.json'  # Cambia esta ruta al nombre de tu archivo
insertar_jugadores_desde_json(ruta_json)

# Cerrar la conexión
conn.close()
