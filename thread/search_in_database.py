import re as regex
from tkinter import ttk
from tkinter import messagebox
from pymongo.database import Database


def SEARCH_IN_DATABASE(
    db: Database,
    search_bar_text: str,
    tree_logs: ttk.Treeview,
    tree_dupeip: ttk.Treeview,
    tree_alts: ttk.Treeview,
    button_buscar: ttk.Button,
):
    # Regex para una dirección IP
    patron_ip = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

    if regex.match(patron_ip, search_bar_text) is None:
        # El regex es un nombre de usuario
        # Ejecutar la query

        # Buscar por jugador
        playername_query = db["player"].find_one(
            {"subplayername": search_bar_text.lower()}
        )
        tree_alts.insert("", "end", values=(str(search_bar_text)))

        if playername_query is None:
            messagebox.showerror(
                "Error",
                "El jugador " + search_bar_text + " no existe o nunca ha entrado.",
            )
            button_buscar.config(state="normal")
            return

        # Buscar la actividad del jugador
        activity_query = (
            db["activity"]
            .find({"subplayername": search_bar_text.lower()})
            .sort("timestamp")
        )
        latest_activity_query = (
            db["latest_activity"]
            .find({"subplayername": search_bar_text.lower()})
            .sort("timestamp")
        )

        # Buscar las ips relacionadas con el jugador
        ip_query = db["ip_address"].find({"subplayername": search_bar_text.lower()})
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
        for activity in latest_activity_query:
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
        ip_query = db["ip_address"].find({"ip": search_bar_text})
        tree_alts.insert("", "end", values=(str(search_bar_text)))

        if ip_query is None:
            messagebox.showerror(
                "Error", "La ip " + ip_query + " no tiene actividad asociada."
            )
            button_buscar.config(state="normal")
            return

        # Buscar los jugadores relacionados con la ip
        player_related_ips: list[str] = []
        for ip_data in ip_query:
            # Poblar la tabla
            tree_dupeip.insert("", "end", values=(str(ip_data["subplayername"])))
            player_related_ips.append(ip_data["subplayername"])

        # Buscar las coincidencias en las ips relacionadas con el jugador
        playername_query = db["player"].find(
            {"subplayername": {"$in": player_related_ips}}
        )

        # Buscar la actividad de los jugadores
        activity_query = (
            db["activity"]
            .find({"subplayername": {"$in": player_related_ips}})
            .sort("timestamp")
        )

        for activity in activity_query:
            tree_logs.insert(
                "",
                "end",
                values=(
                    str(activity["timestamp"]),
                    str(activity["text"]).replace("\n", " "),
                ),
            )
    button_buscar.config(state="normal")
