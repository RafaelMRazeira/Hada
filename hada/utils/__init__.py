# Hada utils package
import json
from hada.consts import DATA_PATH


def load_data():
    f = open(DATA_PATH)
    return json.load(f)


DATA = load_data()
