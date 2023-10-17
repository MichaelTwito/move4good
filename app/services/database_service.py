from __future__ import annotations

import time
from typing import List
from starlette import status
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from api.input_objects_schemas import Order, DeliveryCenter, UpdateOrderModel
from clients.db_client import DBclient
from repositories.tables import OrdersTable,DeliveryCentersTable, UsersTable
from uuid import uuid4
from utils.utils import instrumented_list_to_list_of_dicts,status_filter_instrumented_list

def list_delivery_centers_for_authenticated_user(db_client: DBclient, username: str, id: str, objects_as_dicts=True) -> DeliveryCenter | None:
    try:
        user = (
            db_client.query(UsersTable)
            .filter_by(username=username)
            .one()
        )
        delivery_centers = \
            db_client.query(
                DeliveryCentersTable
                ).filter_by(user_id=user.id).all()\
            if not id else \
            db_client.query(
                DeliveryCentersTable
                ).filter_by(user_id=user.id, id=id).all()
        
    except Exception:
        return None
    return\
        instrumented_list_to_list_of_dicts(
                                            delivery_centers
                                            )\
                                        if objects_as_dicts else delivery_centers

#Optimize the query form the DB, add where caluse to status==opened
def list_delivery_centers(db_client: DBclient, id: str) -> List[DeliveryCenter] | None:
    try:
        #Filter out all the HAMAL ONLY fields
        blacklist = ['description','dropoff_lat', 'dropoff_lng', 'last_updated_at', 'delivery_center_id', 'last_updated_at', 'status']
        if id:
            delivery_centers = \
                            db_client.query(
                                            instance=DeliveryCentersTable
                                            ).all()
            list_of_orders = status_filter_instrumented_list(delivery_centers[0].orders, blacklist)
            dict_to_append = \
                {"orders": instrumented_list_to_list_of_dicts(list_of_orders, blacklist)}
        else: 
            delivery_centers = db_client.query(DeliveryCentersTable).all()
            dict_to_append = {}
    except Exception:
        return None
    return [
            {**{
                "id": delivery_center.id,
                "name": delivery_center.name,
                "address": delivery_center.address,
                "lat": delivery_center.lat,
                "lng": delivery_center.lng
            },** dict_to_append}
            for delivery_center in delivery_centers
            ]

def create_delivery_center(db_client: DBclient, delivery_center: DeliveryCenter, username: str) -> JSONResponse:
    try:

        user = db_client.query(UsersTable).filter_by(username=username).one()
        
        delivery_center = DeliveryCentersTable(
                                                id = str(uuid4()),
                                                name=delivery_center.name, 
                                                address=delivery_center.address, 
                                                lat = delivery_center.lat,
                                                lng = delivery_center.lng, 
                                                user=user
                                                )
        db_client.add(delivery_center)
        db_client.commit()

    except Exception as e:
        db_client.rollback()
        return None
    return {"id": delivery_center.id,
            "name": delivery_center.name,
            "address": delivery_center.address,
            "lat": delivery_center.lat,
            "lng": delivery_center.lng
            }


def update_order(db_client: DBclient, order_id: str, update_data: UpdateOrderModel):
    try:
        # Retrieve the existing order by ID
        existing_order = db_client.query(OrdersTable).filter(OrdersTable.id == order_id).first()

        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Define the list of field names (which are the same as attribute names)
        field_to_attr_mapping = [
            "contact_number",
            "size_description",
            "dropoff_address",
            "status",
            "description",
            "dropoff_lat",
            "dropoff_lng",
            "delivery_center_id",
        ]
        
        # Update the fields with new data if they are provided in the update_data
        for field_name in field_to_attr_mapping:
            field_value = getattr(update_data, field_name)
            if field_value is not None:
                setattr(existing_order, field_name, field_value)

        # Update the 'last_updated_at' timestamp
        existing_order.last_updated_at = int(time.time())

        db_client.commit()
    except Exception:
        db_client.rollback()
        return None
    return {
            "id": existing_order.id,
            "contact_number": existing_order.contact_number,
            "size_description": existing_order.size_description,
            "description": existing_order.description,
            "dropoff_address": existing_order.dropoff_address,
            "status": jsonable_encoder(existing_order.status),
            "dropoff_lat": existing_order.dropoff_lat,
            "dropoff_lng": existing_order.dropoff_lng,
            "created_at": existing_order.created_at,
            "last_updated_at": existing_order.last_updated_at
            }
                         
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
            dropoff_adderss = order.dropoff_address,
            dropoff_lat = order.dropoff_lat,
            dropoff_lng = order.dropoff_lng,
            created_at = order.created_at,
            last_updated_at = order.last_updated_at,
            delivery_center_id = order.delivery_center_id,
            delivery_center = DeliveryCenter(lat=order.delivery_center.lat, lng=order.delivery_center.lng).dict()
            )
            for order in orders
          ]

def create_order(db_client: DBclient, username, order: Order) -> JSONResponse:
    try:
        delivery_center =\
            list_delivery_centers_for_authenticated_user(
                db_client=db_client,
                username=username,
                id=order.delivery_center_id,
                objects_as_dicts=False
                )[0]
        
        if not delivery_center:
            raise Exception

        epoch_time_in_miliseconds = int(time.time())
        new_record = OrdersTable(
            id = str(uuid4()),
            contact_number = order.contact_number,
            size_description = order.size_description,
            dropoff_address = order.dropoff_address,
            dropoff_lat = order.dropoff_lat,
            dropoff_lng = order.dropoff_lng,
            created_at = epoch_time_in_miliseconds,
            last_updated_at = epoch_time_in_miliseconds,
            delivery_center = delivery_center,
        )
        if 'description' in dir(order):
            setattr(new_record, 'description', order.description)
            optional_dict_to_append = {'description': order.description}
        else:
            optional_dict_to_append = {}
        db_client.add(new_record)
        db_client.commit()
    except Exception:
        db_client.rollback()
        return None
    return {**{"id": new_record.id,
                         "contact_number": new_record.contact_number,
                         "size_description": new_record.size_description,
                         "dropoff_address": new_record.dropoff_address,
                         "status": jsonable_encoder(new_record.status),
                         "dropoff_lat": new_record.dropoff_lat,
                         "dropoff_lng": new_record.dropoff_lng,
                         "created_at": new_record.created_at,
                         "last_updated_at": new_record.last_updated_at}, **optional_dict_to_append}
                          
