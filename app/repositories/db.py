from typing import List
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.tables import Base
from starlette.responses import JSONResponse
from repositories.enteties import User,Order

class OrdersDB(ABC):
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
    def get_reports(self) -> List[Order]:
        raise NotImplemented()

    @abstractmethod
    def update(self, report: Order) -> int:
        raise NotImplemented()

    @abstractmethod
    def delete(self, report_id: str) -> int:
        raise NotImplemented()


class DBclient():
    def __init__(self, connection: str):
        self.engine = create_engine(connection)
        Base.metadata.create_all(self.engine)

        self._Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.session = self._Session()


    def get_orders(self) -> List[Order] | None:
        try:
            sql_reports = self._session.query(OrdersTable)
        except Exception:
            return None
        return [
            Order(
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

    def create(self, report: Order) -> int:
        try:
            current_time = time.time()
            datetime_object = datetime.fromtimestamp(current_time)
            new_record = OrdersTable(
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

    def update(self, report: Order) -> int:
        try:
            sql_report = (
                self._session.query(OrdersTable).filter_by(id=report.id).one()
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
                self._session.query(OrdersTable).filter_by(id=report_id).one()
            )
        except NoResultFound:
            return status.HTTP_404_NOT_FOUND

        self._session.delete(sql_report)
        self._session.commit()

        return status.HTTP_204_NO_CONTENT
