import sqlite3
from gui.logger_dialog import CREATE_GUI
from database.create_database import CREATE_DATABASE_TABLES

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

CREATE_DATABASE_TABLES(cur)
CREATE_GUI(cur)

con.close()
