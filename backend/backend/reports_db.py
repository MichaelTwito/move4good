from abc import ABC, abstractmethod
from typing import List

from backend.report import PartialReport, Report, User


class ReportsDB(ABC):
    @abstractmethod
    def login(self, user: User) -> str:
        raise NotImplemented()
    
    @abstractmethod
    def auth_user(self, token: str) -> bool:
        raise NotImplemented()
    
    @abstractmethod
    def auth_admin(self, token: str) -> bool:
        raise NotImplemented()

    @abstractmethod
    def get_reports(self) -> List[Report]:
        raise NotImplemented()

    @abstractmethod
    def create(self, report: PartialReport) -> int:
        raise NotImplemented()

    @abstractmethod
    def update(self, report: Report) -> int:
        raise NotImplemented()

    @abstractmethod
    def delete(self, report_id: str) -> int:
        raise NotImplemented()
