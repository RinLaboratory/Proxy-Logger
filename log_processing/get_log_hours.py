import re as regex
from datetime import datetime


# Función para obtener la fecha y hora de una línea de log
def GET_LOG_DATEHOURS(line: str, log_filename: str):
    hour_pattern = r"\[(\d+:\d+:\d+)\]"
    date_pattern = r"(\d{4}-\d{2}-\d{2})"

    hour_coincidence = regex.search(hour_pattern, line)
    date_coincidence = regex.search(date_pattern, log_filename)

    if hour_coincidence and date_coincidence:
        fecha_str = date_coincidence.group(1) + " " + hour_coincidence.group(1)
        return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    else:
        return None
