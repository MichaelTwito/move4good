import jwt
import time
from hashlib import sha256
from secrets import compare_digest
from sqlalchemy.exc import NoResultFound
from config.config import ConfigClass
from repositories.tables import UsersTable
from repositories.enteties import User

def login(self, user: User) -> str:
    try:
        sql_user = (
            self._session.query(UsersTable)
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
    except:
        self._session.rollback()

    encoded_jwt = jwt.encode(
        {
            ConfigClass.JWT_USERNAME: user.username,
            ConfigClass.JWT_EXPIRES: int(time.time()) + ConfigClass.JWT_EXPIRE_TIME,
            ConfigClass.JWT_ROLE: sql_user.role,
        },
        ConfigClass.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt