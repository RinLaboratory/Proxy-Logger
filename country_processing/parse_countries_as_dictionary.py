from utils.types import TypesCountryDictionary
from country_processing.load_countries import LOAD_COUNTRIES


def PARSE_COUNTRIES_AS_DICTIONARY():
    # country name ; ISO2 code
    country_dictionary: TypesCountryDictionary = {
        "spanish": {},
        "english": {},
    }

    file_lines = LOAD_COUNTRIES()

    for line in file_lines:
        if file_lines.index(line) != 0:
            splitted_line = line.replace("\n", "").replace('"', "").split(",")
            es_country_name = splitted_line[0]
            en_country_name = splitted_line[1]
            iso2_country = splitted_line[3]
            country_dictionary["spanish"] = {
                **country_dictionary["spanish"],
                es_country_name: (es_country_name, iso2_country),
            }
            country_dictionary["english"] = {
                **country_dictionary["english"],
                en_country_name: (en_country_name, iso2_country),
            }

    return country_dictionary
