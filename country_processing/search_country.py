import re
from utils.types import TypesCountryDictionary


def SEARCH_COUNTRY(country_name: str, country_dictionary: TypesCountryDictionary):
    pattern = re.compile(re.escape(country_name), re.IGNORECASE)
    for country in country_dictionary["english"].keys():
        if pattern.search(country):
            return country_dictionary["english"][country][1]
    for country in country_dictionary["spanish"].keys():
        if pattern.search(country):
            return country_dictionary["spanish"][country][1]
    print("none result for: " + country_name)
    return None
