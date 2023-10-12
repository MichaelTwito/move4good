from __future__ import annotations

import pytz
import datetime
from typing import List
from starlette import status
from starlette.responses import JSONResponse
from repositories.enteties import Order, DeliveryCenter
from repositories.db import DBclient
from repositories.tables import OrdersTable,DeliveryCenterTable
from uuid import uuid4

def list_delivery_centers(db_client: DBclient) -> List[DeliveryCenter] | None:
    try:
        delivery_centers = db_client.query(DeliveryCenterTable)
    
    except Exception:
        return None
    return [
            DeliveryCenter(
                id = delivery_center.id,
                lat = delivery_center.lat,
                lng = delivery_center.lng
            )
            for delivery_center in delivery_centers
            ]

def create_delivery_center(db_client: DBclient, delivery_center: DeliveryCenter) -> JSONResponse:
    try:
        new_record = DeliveryCenter(
                lat = delivery_center.lat,
                lng = delivery_center.lng
                )
        db_client._session.add(new_record)
        db_client._Session.commit()
    except Exception as e:
        print(e)
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse({"id": new_record.id,
                         "lat": new_record.lat,
                         "lng": new_record.lng,
                         "orders": new_record.orders
                         },
                          status_code=status.HTTP_201_CREATED)

def list_orders(db_client: DBclient) -> List[Order] | None:
    try:
        orders = db_client.query(OrdersTable)
    except Exception:
        return None
    return [
            Order(
            id = order.id,
            contact_number = order.contact_number,
            size_description = order.size_description,
            status = order.status,
            dropoff_lat = order.dropoff_lat,
            dropoff_lng = order.dropoff_lng,
            created_at = order.created_at,
            last_updated_at = order.last_updated_at,
            delivery_center_id = order.delivery_center_id,
            delivery_center = order.delivery_center
            )
            for order in orders
          ]

def create_order(db_client: DBclient, order: Order) -> JSONResponse:
    try:
        israel_timezone = pytz.timezone('Asia/Jerusalem')
        datetime_object = datetime.datetime.now(israel_timezone)
        new_record = OrdersTable(
            id = str(uuid4()),
            contact_number = order.contact_number,
            size_description = order.size_description,
            status = order.status,
            dropoff_lat = order.dropoff_lat,
            dropoff_lng = order.dropoff_lng,
            created_at = datetime_object,
            last_updated_at = datetime_object,
            delivery_center = DeliveryCenterTable(id=order.delivery_center_id,lat=order.delivery_center.lat, lng=order.delivery_center.lng),
        )
        new_record.delivery_center_id = new_record.delivery_center.id
        db_client.add(new_record)
        db_client.commit()
    except Exception as e:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse({"id": new_record.id,
                         "contact_number": new_record.contact_number,
                         "size_description": new_record.size_description,
                         "status": new_record.status,
                         "dropoff_lat": new_record.dropoff_lat,
                         "dropoff_lng": new_record.dropoff_lng,
                         "created_at": new_record.created_at.isoformat(),
                         "last_updated_at": new_record.last_updated_at.isoformat()},
                          status_code=status.HTTP_201_CREATED)
# def update_order(DBclient, report: Order) -> int:
#     try:
#         sql_report = (
#             self._session.query(OrdersTable).filter_by(id=report.id).one()
#         )
#     except NoResultFound:
#         return status.HTTP_404_NOT_FOUND
    
#     sql_report.description = report.description
#     sql_report.lng = report.lng
#     sql_report.lat = report.lat
#     sql_report.type = report.type.value
#     sql_report.report_amount = report.report_amount
#     self._session.commit()

#     return JSONResponse({"id": sql_report.id,
#                         "lng": sql_report.lng,
#                         "lat": sql_report.lat,
#                         "type": sql_report.type,
#                         "description": sql_report.description,
#                         "report_amount": sql_report.report_amount,
#                         "created_at": str(sql_report.time)}, status_code=status.HTTP_201_CREATED)
# def delete_order(DBclient, report_id: str) -> int:
    try:
        sql_report = (
            self._session.query(OrdersTable).filter_by(id=report_id).one()
        )
    except NoResultFound:
        return status.HTTP_404_NOT_FOUND
    self._session.delete(sql_report)
    self._session.commit()
    return status.HTTP_204_NO_CONTENT