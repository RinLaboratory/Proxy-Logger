import sqlite3

def CREATE_DATABASE_TABLES(cur: sqlite3.Cursor):
    cur.execute("CREATE TABLE IF NOT EXISTS player(id INTEGER PRIMARY KEY AUTOINCREMENT, playername TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS file(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, proxy_type TEXT, hash TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS activity(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, timestamp TEXT, player_id INTEGER, file_id INTEGER, FOREIGN KEY(player_id) REFERENCES player(id), FOREIGN KEY(file_id) REFERENCES file(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS ip_address(id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS player_ip(player_id INTEGER, ip_id INTEGER, FOREIGN KEY(player_id) REFERENCES player(id), FOREIGN KEY(ip_id) REFERENCES ip_address(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS nlogin(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, player_id INTEGER, FOREIGN KEY(player_id) REFERENCES player(id))")