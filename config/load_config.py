import yaml
from utils.types import TypesConfig


def LOAD_CONFIG(file_path: str):
    with open(file_path, "r") as file:
        config: TypesConfig = yaml.safe_load(file)
    return config
