import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('jugadores.db')
cursor = conn.cursor()

# Consulta para obtener todos los equipos
cursor.execute("SELECT team_label FROM players")
equipos = cursor.fetchall()

for equipo in equipos:
    original_name = equipo[0]
    updated_name = original_name  # Inicializa el nombre actualizado como el original

    if original_name.lower() == 'man utd':
        updated_name = 'Manchester United'
    elif original_name.lower() == 'spurs':
        updated_name = 'Tottenham Hotspur'
    elif original_name.lower() == 'notting. forest':
        updated_name = 'Nottingham Forest'
    elif original_name.lower() == 'newcastle utd':
        updated_name = 'Newcastle United'

    # Solo actualiza si hay un cambio
    if updated_name != original_name:
        cursor.execute("""
            UPDATE players 
            SET team_label = ? 
            WHERE team_label = ?
        """, (updated_name, original_name))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Actualización de nombres completada.")
