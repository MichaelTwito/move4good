from time import time
from jwt import decode, InvalidTokenError
from repositories.enteties import RolesType
from config.config import ConfigClass

def auth_user(token: str) -> bool:
    return auth(token, RolesType.normal)

def auth_admin(token: str) -> bool:
    return auth(token, RolesType.admin)

def auth(token: str, role: RolesType) -> bool:
    try:
        decoded_jwt = decode(
            token, ConfigClass.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        if decoded_jwt.get(ConfigClass.JWT_EXPIRES) < time():
            return False
        # admin always passes
        if int(decoded_jwt.get(ConfigClass.JWT_ROLE)) == int(RolesType.admin):
            return True
        if not int(decoded_jwt.get(ConfigClass.JWT_ROLE)) == int(role):
            return False
    except InvalidTokenError:
        return False
    return True
