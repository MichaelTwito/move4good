from __future__ import annotations

import time
import datetime
from datetime import datetime
from secrets import compare_digest
from hashlib import sha256
from typing import List
from uuid import uuid4

import jwt
from jwt import InvalidTokenError
from starlette.responses import JSONResponse
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette import status


from backend.consts import (
    JWT_EXPIRES,
    JWT_EXPIRE_TIME,
    JWT_ROLE,
    JWT_SECRET_KEY,
    JWT_USERNAME,
    PASSWORD_PEPPER,
    ORDERS_TABLE_NAME,
    USERS_TABLE_NAME,
)
from backend.report import Report, User, RolesType
from backend.reports_db import ReportsDB

Base = declarative_base()


class UsersTable(Base):
    __tablename__ = USERS_TABLE_NAME
    username = Column(String(255), primary_key=True, index=True)
    password = Column(String(255))
    role = Column(String(255))


class OrdersTable(Base):
    __tablename__ = ORDERS_TABLE_NAME
    id = Column(String(255), primary_key=True, index=True)
    description = Column(String(255))
    lat = Column(String(255))
    lng = Column(String(255))
    type = Column(String(255))
    time = Column(DateTime)
    report_amount = Column(Integer)

class Config:
    orm_mode = True


class SqlReportsDB(ReportsDB):
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
            password_cipher.update(PASSWORD_PEPPER.encode())

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
                JWT_USERNAME: user.username,
                JWT_EXPIRES: int(time.time()) + JWT_EXPIRE_TIME,
                JWT_ROLE: sql_user.role,
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return encoded_jwt

    def auth_user(self, token: str) -> bool:
        return self._auth(token, RolesType.normal)

    def auth_admin(self, token: str) -> bool:
        return self._auth(token, RolesType.admin)

    def _auth(self, token: str, role: RolesType) -> bool:
        try:
            decoded_jwt = jwt.decode(
                token, JWT_SECRET_KEY, algorithms=["HS256"]
            )

            if decoded_jwt.get(JWT_EXPIRES) < time.time():
                return False

            # admin always passes
            if int(decoded_jwt.get(JWT_ROLE)) == int(RolesType.admin):
                return True

            if not int(decoded_jwt.get(JWT_ROLE)) == int(role):
                return False
        except InvalidTokenError:
            return False

        return True

    def get_reports(self) -> List[Report] | None:
        try:
            sql_reports = self._session.query(ReportsTable)
        except Exception:
            return None
        return [
            Report(
                description=report.description,
                lat=report.lat,
                lng=report.lng,
                type=report.type,
                id=report.id,
                time=report.time,
                report_amount=report.report_amount
            )
            for report in sql_reports
        ]

    def create(self, report: Report) -> int:
        try:
            current_time = time.time()
            datetime_object = datetime.fromtimestamp(current_time)
            new_record = ReportsTable(
                id=str(uuid4()),
                description=report.description,
                lat=str(report.lat),
                lng=str(report.lng),
                type=int(report.type),
                time=datetime_object,
                report_amount=report.report_amount
            )
            self._session.add(new_record)
            self._session.commit()
        except Exception:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

        return JSONResponse({"id": new_record.id,
                             "description": new_record.description,
                             "lat": new_record.lat,
                             "lng": new_record.lng,
                             "type": new_record.type,
                             "report_amount": new_record.report_amount,
                             "created_at": str(new_record.time),
                            }, status_code=status.HTTP_201_CREATED)

    def update(self, report: Report) -> int:
        try:
            sql_report = (
                self._session.query(ReportsTable).filter_by(id=report.id).one()
            )
        except NoResultFound:
            return status.HTTP_404_NOT_FOUND
        
        sql_report.description = report.description
        sql_report.lng = report.lng
        sql_report.lat = report.lat
        sql_report.type = report.type.value
        sql_report.report_amount = report.report_amount
        self._session.commit()

        return JSONResponse({"id": sql_report.id,
                            "lng": sql_report.lng,
                            "lat": sql_report.lat,
                            "type": sql_report.type,
                            "description": sql_report.description,
                            "report_amount": sql_report.report_amount,
                            "created_at": str(sql_report.time)}, status_code=status.HTTP_201_CREATED)

    def delete(self, report_id: str) -> int:
        try:
            sql_report = (
                self._session.query(ReportsTable).filter_by(id=report_id).one()
            )
        except NoResultFound:
            return status.HTTP_404_NOT_FOUND

        self._session.delete(sql_report)
        self._session.commit()

        return status.HTTP_204_NO_CONTENT
