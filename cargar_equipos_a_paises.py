import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('jugadores.db')
cursor = conn.cursor()

# Paso 1: Agregar la columna 'team_country' si no existe
try:
    cursor.execute("ALTER TABLE players ADD COLUMN team_country TEXT")
    print("Columna 'team_country' agregada con éxito.")
except sqlite3.OperationalError:
    print("La columna 'team_country' ya existe.")

# Paso 2: Lista de equipos ingleses
equipos_ingleses = [
    'arsenal', 'aston villa', 'afc bournemouth', 'brighton', 'manchester city',
    'manchester united', 'liverpool', 'everton', 'newcastle united', 'nottingham forest',
    'tottenham hotspur', 'southampton', 'brentford', 'leicester city', 'ipswich town',
    'west ham', 'chelsea', 'fulham', 'crystal palace', 'wolves'
]

# Paso 3: Asignar 'inglaterra' a los equipos ingleses
for equipo in equipos_ingleses:
    cursor.execute("""
        UPDATE players
        SET team_country = 'Inglaterra'
        WHERE LOWER(team_label) = ?
    """, (equipo,))
    print(f"Campo 'team_country' actualizado para el equipo {equipo.capitalize()}")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
print("Actualización completada.")
