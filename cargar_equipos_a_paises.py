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

# Paso 2: Asignar 'Espana' a los equipos españoles
equipos_espanoles = ['Atlético de Madrid', 'FC Barcelona','Real Madrid','Athletic Club']  # Lista de equipos españoles
for equipo in equipos_espanoles:
    cursor.execute("""
        UPDATE players
        SET team_country = 'Espana'
        WHERE LOWER(team_label) = ?
    """, (equipo.lower(),))  # Cambia a minúsculas para la comparación
    print(f"Campo 'team_country' actualizado para el equipo {equipo}")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
print("Actualización completada.")
