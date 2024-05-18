import os
from gui.logger_dialog import CREATE_GUI
from config.save_config import CONFIG_FILE
from gui.ask_database_details_dialog import ASK_DATABASE_DETAILS_DIALOG
from config.load_config import LOAD_CONFIG
from database.get_database import GET_DATABASE


if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        ASK_DATABASE_DETAILS_DIALOG()
    else:
        print("El archivo de configuración ya existe.")

        config: dict[str, str] = LOAD_CONFIG(CONFIG_FILE)
        db = GET_DATABASE(config["mongodb_connection_string"])
        CREATE_GUI(db, config)
