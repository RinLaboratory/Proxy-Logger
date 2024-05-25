import json

# Ruta del archivo de configuración
CONFIG_FILE: str = "config.json"


def SAVE_CONFIG(connection_string: str):
    # Guarda la cadena de conexión en el archivo de configuración.
    config = {"mongodb_connection_string": connection_string}
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
