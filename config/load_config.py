import yaml


def LOAD_CONFIG(file_path: str):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config
