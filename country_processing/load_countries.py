def LOAD_COUNTRIES():
    with open(
        "./country_processing/spanish-countries.csv", "r", encoding="utf8"
    ) as file:
        return file.readlines()
