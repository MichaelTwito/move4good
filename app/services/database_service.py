from __future__ import annotations

import pytz
import datetime
from typing import List
from starlette import status
from starlette.responses import JSONResponse
from repositories.enteties import Order, DeliveryCenter
from repositories.db import DBclient
from repositories.tables import OrdersTable,DeliveryCentersTable, UsersTable
from uuid import uuid4
from utils.utils import instrumented_list_to_list_of_dicts


def get_delivery_center(db_client: DBclient, id: str,parse_to_json_reponse=True) -> DeliveryCenter | None:
    try:
        delivery_center = \
            db_client.query(
                DeliveryCentersTable
                ).filter_by(id=id).one()
    except Exception:
        return None
    return  JSONResponse({"id": delivery_center.id,
                         "lat": delivery_center.lat,
                         "lng": delivery_center.lng,
                         "orders": instrumented_list_to_list_of_dicts(delivery_center.orders)
                         },
                          status_code=status.HTTP_201_CREATED) if parse_to_json_reponse\
                                                                     else delivery_center

def list_delivery_centers(db_client: DBclient) -> List[DeliveryCenter] | None:
    try:
        delivery_centers = db_client.query(DeliveryCentersTable)
    
    except Exception:
        return None
    return [
            DeliveryCenter(
                id = delivery_center.id,
                lat = delivery_center.lat,
                lng = delivery_center.lng,
                users = UsersTable()
            )
            for delivery_center in delivery_centers
            ]

def create_delivery_center(db_client: DBclient, delivery_center: DeliveryCenter, username: str) -> JSONResponse:
    try:
        user = db_client.query(UsersTable).filter_by(username=username).one()
        new_record = DeliveryCentersTable(id = str(uuid4()), lat = delivery_center.lat,lng = delivery_center.lng, user=user)
        db_client.add(new_record)
        db_client.commit()
    except Exception:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse({"id": new_record.id,
                         "lat": new_record.lat,
                         "lng": new_record.lng
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
            delivery_center = DeliveryCenter(lat=order.delivery_center.lat, lng=order.delivery_center.lng).dict()
            )
            for order in orders
          ]


def create_order(db_client: DBclient, order: Order) -> JSONResponse:
    try:
        delivery_center = get_delivery_center(db_client, order.delivery_center_id, False)
        if not delivery_center:
            delivery_center = DeliveryCentersTable(id=order.delivery_center_id,lat=order.delivery_center.lat,lng=order.delivery_center.lng)

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
            delivery_center = delivery_center,
        )
        new_record.delivery_center_id = delivery_center.id
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
