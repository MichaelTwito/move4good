from jwt import decode
from datetime import datetime
from config.config import ConfigClass
from fastapi.encoders import jsonable_encoder
from repositories.enteties import StatusEnum
def get_username_from_token(token: str):
    decoded_jwt = decode(
            token, ConfigClass.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    return decoded_jwt['username']


def instrumented_list_to_list_of_dicts(instrumented_list, blacklist=[]):
    list_of_dicts = []
    for item in instrumented_list:
        if 'status' in blacklist and item.__dict__['status'] != StatusEnum.OPENED:
            continue
        dict_item = {}
        for key in item.__dict__.keys():
            if not key.startswith("_") and key not in blacklist:
                value = getattr(item, key)
                if isinstance(value, StatusEnum):
                    value = jsonable_encoder(value)
                dict_item[key] = value
        
        list_of_dicts.append(dict_item)
    return list_of_dicts
