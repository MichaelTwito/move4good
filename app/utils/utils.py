from jwt import decode
from config.config import ConfigClass
from fastapi.encoders import jsonable_encoder
from api.input_objects_schemas import StatusEnum

def get_username_from_token(token: str):
    decoded_jwt = decode(
            token, ConfigClass.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    return decoded_jwt['username']

def status_filter_instrumented_list(instrumented_list, blacklist=[]):
    status_filter = [StatusEnum.DELETED]
    if 'status' in blacklist:
        status_filter.extend([StatusEnum.ASSIGNED, StatusEnum.PICKED_UP, StatusEnum.COMPLETE])
    return filter(lambda item: item.__dict__['status'] not in status_filter,instrumented_list)

def instrumented_list_to_list_of_dicts(instrumented_list: list, blacklist=[]):
    list_of_dicts = []
    for item in instrumented_list:
        dict_item = {}
        for key in item.__dict__.keys():
            if not key.startswith("_") and key not in blacklist:
                value = getattr(item, key)
                if isinstance(value, StatusEnum):
                    value = jsonable_encoder(value)
                dict_item[key] = value
        
        if 'orders' in dir(item):
            filtered_orders = status_filter_instrumented_list(item.orders)
            dict_item = {**dict_item,
             **{'orders':
                instrumented_list_to_list_of_dicts(filtered_orders)
                }
            }
        list_of_dicts.append(dict_item)
    return list_of_dicts
