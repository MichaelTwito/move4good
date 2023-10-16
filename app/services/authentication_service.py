from time import time
from jwt import encode
from hashlib import sha256
from secrets import compare_digest
from repositories.tables import UsersTable
from api.input_objects_schemas import User
from config.config import ConfigClass
from sqlalchemy.exc import NoResultFound
from clients.db_client import DBclient
from jwt import decode, InvalidTokenError
from api.input_objects_schemas import RolesType
from config.config import ConfigClass

def login(db_client: DBclient, user: User) -> str:
    try:
        sql_user = (
            db_client.query(UsersTable)
            .filter_by(username=user.username)
            .one()
        )
        password_cipher = sha256()
        password_cipher.update(user.password.encode())
        password_cipher.update(ConfigClass.PASSWORD_PEPPER.encode())
        if not compare_digest(
            password_cipher.hexdigest(), sql_user.password
        ):
            return ""
    except NoResultFound:
        return ""
    except Exception:
        db_client.session.rollback()
    encoded_jwt = encode(
        {
            ConfigClass.JWT_USERNAME: user.username,
            ConfigClass.JWT_EXPIRES: int(time()) + ConfigClass.JWT_EXPIRE_TIME,
            ConfigClass.JWT_ROLE: sql_user.role,
        },
        ConfigClass.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt

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
