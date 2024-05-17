import sqlite3
import re as regex
from tkinter import ttk
from datetime import datetime


def SEARCH(
    cur: sqlite3.Cursor,
    entry_input: ttk.Entry,
    tree_logs: ttk.Treeview,
    tree_dupeip: ttk.Treeview,
    tree_alts: ttk.Treeview,
):
    # Aquí implementarás la lógica para buscar según el nombre de usuario o dirección IP
    search_bar_text = entry_input.get()
    print(search_bar_text)

    # Borrar todos los elementos de las tablas
    for i in tree_logs.get_children():
        tree_logs.delete(i)
    for i in tree_dupeip.get_children():
        tree_dupeip.delete(i)

    # Regex para una dirección IP
    patron_ip = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if regex.match(patron_ip, search_bar_text) is None:
        # El regex es un nombre de usuario
        # Ejecutar la query
        query_log: list[tuple[datetime, str, str, str, int]] = cur.execute(
            "SELECT activity.timestamp, activity.text, ip_address.ip, player.playername, activity.id AS activity_id \
                                FROM activity \
                                INNER JOIN player ON activity.player_id = player.id \
                                LEFT JOIN player_ip ON player.id = player_ip.player_id \
                                LEFT JOIN ip_address ON player_ip.ip_id = ip_address.id \
                                WHERE player.playername = ? \
                                ORDER BY datetime(activity.timestamp, 'localtime')",
            (search_bar_text,),
        ).fetchall()

        ips: list[str] = []
        activity: list[int] = []
        tree_alts.insert("", "end", values=(str(search_bar_text)))
        # Mostrar resultados en la tabla de logs relacionados
        for timestamp, log_activity, ip, playername, activity_id in query_log:
            if activity_id and activity_id not in activity:
                tree_logs.insert(
                    "",
                    "end",
                    values=(str(timestamp), str(log_activity).replace("\n", " ")),
                )
                activity.append(activity_id)
            if ip and ip not in ips:
                tree_dupeip.insert("", "end", values=(str(ip)))
                ips.append(ip)
    else:
        # El regex es una IP
        # Ejecutar la query
        query_log: list[tuple[datetime, str, str, str, int]] = cur.execute(
            "SELECT activity.timestamp, activity.text, ip_address.ip, player.playername, activity.id AS activity_id \
                                FROM activity \
                                INNER JOIN player ON activity.player_id = player.id \
                                LEFT JOIN player_ip ON player.id = player_ip.player_id \
                                LEFT JOIN ip_address ON player_ip.ip_id = ip_address.id \
                                WHERE ip_address.ip = ? \
                                ORDER BY datetime(activity.timestamp, 'localtime')",
            (search_bar_text,),
        ).fetchall()

        player: list[str] = []
        activity: list[int] = []
        tree_alts.insert("", "end", values=(str(search_bar_text)))
        # Mostrar resultados en la tabla de logs relacionados
        for timestamp, log_activity, ip, playername, activity_id in query_log:
            if activity_id and activity_id not in activity:
                tree_logs.insert(
                    "",
                    "end",
                    values=(str(timestamp), str(log_activity).replace("\n", " ")),
                )
                activity.append(activity_id)
            if playername and playername not in player:
                tree_dupeip.insert("", "end", values=(str(playername)))
                player.append(playername)
