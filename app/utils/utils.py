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


def instrumented_list_to_list_of_dicts(instrumented_list, convert_datetime=True):
    list_of_dicts = []
    for item in instrumented_list:
        dict_item = {}
        for key in item.__dict__.keys():
            if not key.startswith("_"):
                value = getattr(item, key)
                if convert_datetime and isinstance(value, datetime):
                    value = value.isoformat()
                if isinstance(value, StatusEnum):
                    value = jsonable_encoder(value)
                dict_item[key] = value
        list_of_dicts.append(dict_item)
    return list_of_dicts
