from __future__ import annotations

from hashlib import sha256
import time
from secrets import compare_digest
from typing import List

import jwt
from pydantic_extra_types.coordinate import Latitude, Longitude
from starlette import status

from backend.report import PartialReport, Report, RolesType, User, ReportsType
from backend.reports_db import ReportsDB
from backend.consts import MOCK_TOKEN, JWT_SECRET_KEY, PASSWORD_PEPPER, MOCK_PASSWORD


class MockReportsDB(ReportsDB):
    def __init__(self):
        self._id = 3
        self._db = {
            "1": Report(
                id="1",
                description="desc",
                lat=Latitude('12.123'),
                lng=Longitude('12.123'),
                type=ReportsType.terrorists,
                time=int(time.time()),
                report_amount=6,

            ),
            "2": Report(
                id="2",
                description="desc",
                lat=Latitude('12.123'),
                lng=Longitude('12.123'),
                type=ReportsType.terrorists,
                time=int(time.time()),
                report_amount=7,
            ),
        }

    def login(self, user: User) -> str | None:
        password_cipher = sha256()
        password_cipher.update(user.password.encode())
        password_cipher.update(PASSWORD_PEPPER.encode())
        print(user.password, password_cipher.hexdigest())
        if compare_digest(password_cipher.hexdigest(), MOCK_PASSWORD):
            return MOCK_TOKEN
        return ""

    def auth(self, token: str) -> bool:
        return token == MOCK_TOKEN
    def auth_admin(self, token: str) -> bool:
        jwt_decode = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return jwt_decode.get('role', RolesType.admin.value) == RolesType.admin.value
    def auth_user(self, token: str) -> bool:
        jwt_decode = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return jwt_decode.get('role', RolesType.normal.value) == RolesType.normal.value
    def get_reports(self) -> List[Report]:
        return list(self._db.values())

    def create(self, report: PartialReport) -> int:
        self._db[f"{self._id}"] = Report(
            id=f"{self._id}",
            description=report.description,
            lat=report.lat,
            lng=report.lng,
            type=report.type,
            time=int(time.time()),
            report_amount=report.report_amount,
        )
        self._id += 1
        return status.HTTP_201_CREATED

    def update(self, report: Report) -> int:
        if not self._db.get(report.id):
            return status.HTTP_404_NOT_FOUND

        old_report = self._db[report.id]

        self._db[report.id] = Report(
            id=old_report.id,
            description=report.description,
            lat=report.lat,
            lng=report.lng,
            type=report.type,
            time=old_report.time,
            report_amount=report.report_amount,
        )
        return status.HTTP_204_NO_CONTENT

    def delete(self, report_id: str) -> int:
        if not self._db.get(report_id):
            return status.HTTP_404_NOT_FOUND

        self._db.pop(report_id)

        return status.HTTP_204_NO_CONTENT
