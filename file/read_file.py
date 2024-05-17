def MERGE_FILE_LINES(lines: list[str]):
        # El archivo posee lineas de enter que muestran mensajes de baneos y errores que deben
        # ser filtrados y colocados como línea única antes de pasarlos por la db para no insertar basura.
        merged_lines: list[str] = []
        current_line = ""
        for line in lines:
            if line.startswith("["):
                if current_line:
                    merged_lines.append(current_line.strip())
                    current_line = ""
            current_line += line.strip() + "\n"
        if current_line:
            merged_lines.append(current_line.strip())
        return merged_lines

def READ_FILE(file_path: str):
        with open(file_path, "r", encoding="utf8") as file:
            return MERGE_FILE_LINES(file.readlines())