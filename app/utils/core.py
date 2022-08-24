from app import db, ma
import datetime

# https://stackoverflow.com/questions/644178/how-do-i-re-map-python-dict-keys
def map_rekey(inp_dict, keys_replace):
    return {keys_replace.get(k, k): v for k, v in inp_dict.items()}


def rename_keys(d, keys):
    # data and translation
    return dict([(keys.get(k), v) for k, v in d.items()])
