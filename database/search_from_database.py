import re as regex
from tkinter import ttk
from pymongo.database import Database


def SEARCH(
    db: Database,
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

        # Buscar por jugador
        playername_query = db["player"].find_one({"playername": search_bar_text})
        tree_alts.insert("", "end", values=(str(search_bar_text)))

        # Buscar la actividad del jugador
        activity_query = (
            db["activity"]
            .find({"player_id": playername_query["_id"]})
            .sort("timestamp")
        )

        # Buscar las ips relacionadas con el jugador
        player_related_ips: list[str] = []
        player_ip_query = db["player_ip"].find({"player_id": playername_query["_id"]})
        for player_ip in player_ip_query:
            player_related_ips.append(player_ip["ip_id"])

        # Buscar las coincidencias en las ips relacionadas con el jugador
        ip_query = db["ip_address"].find({"_id": {"$in": player_related_ips}})

        # Poblar la tabla
        for ip in ip_query:
            tree_dupeip.insert("", "end", values=(str(ip["ip"])))

        for activity in activity_query:
            tree_logs.insert(
                "",
                "end",
                values=(
                    str(activity["timestamp"]),
                    str(activity["text"]).replace("\n", " "),
                ),
            )

    else:
        # Buscar por ip
        ip_query = db["ip_address"].find_one({"ip": search_bar_text})
        tree_alts.insert("", "end", values=(str(search_bar_text)))

        # Buscar los jugadores relacionados con la ip
        player_related_ips: list[str] = []
        player_data_query = db["player_ip"].find({"ip_id": ip_query["_id"]})
        for player_data in player_data_query:
            player_related_ips.append(player_data["player_id"])

        # Buscar las coincidencias en las ips relacionadas con el jugador
        playername_query = db["player"].find({"_id": {"$in": player_related_ips}})

        # Buscar la actividad de los jugadores
        activity_query = (
            db["activity"]
            .find({"player_id": {"$in": player_related_ips}})
            .sort("timestamp")
        )

        # Poblar la tabla
        for playername in playername_query:
            tree_dupeip.insert("", "end", values=(str(playername["playername"])))

        for activity in activity_query:
            tree_logs.insert(
                "",
                "end",
                values=(
                    str(activity["timestamp"]),
                    str(activity["text"]).replace("\n", " "),
                ),
            )
