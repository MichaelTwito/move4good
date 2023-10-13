import jwt
import time
from hashlib import sha256
from secrets import compare_digest
from sqlalchemy.exc import NoResultFound
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.tables import Base
from repositories.enteties import User
from config.config import ConfigClass
from repositories.tables import UsersTable

class DBclient():
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        Base.metadata.create_all(self.engine)

        self._Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._session = self._Session()


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

    def add(self, instance):
        self._session.add(instance)

    def commit(self):
        self._session.commit()


    def query(self, instance):
        return self._session.query(instance)
