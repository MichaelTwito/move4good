from repositories.db import DBclient
from fastapi import Body, Depends, HTTPException, APIRouter, Header
from starlette import status
from typing import List
from starlette.requests import Request
from services import database_service
from config.config import ConfigClass
from repositories.enteties import User,Order, DeliveryCenter
from services.authentication_service import auth_user, auth_admin
from utils.utils import get_username_from_token
router = APIRouter()
APP_DB= DBclient(ConfigClass.SQL_CONNECTION_STRING)

async def auth_user(request: Request):
    auth_token = request.headers.get(ConfigClass.REQUESTS_AUTH_TOKEN)
    if not (auth_token and auth_user(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

async def auth_admin(request: Request):
    auth_token = request.headers.get(ConfigClass.REQUESTS_AUTH_TOKEN)
    if not (auth_token and auth_admin(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

@router.post("/api/login", response_model=str)
async def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
):

    token = APP_DB.login(User(username=username, password=password))
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    return token

@router.get(
    "/api/orders/all",
    dependencies=[Depends(auth_user)],
    response_model=List[Order],
)
async def list_orders():
    return database_service.list_orders(APP_DB)


@router.get(
    "/api/delivery_centers",
    response_model=DeliveryCenter
)
async def get_delivery_center(id: str):
    return database_service.get_delivery_center(APP_DB, id)

@router.post(
    "/api/create_order",
    dependencies=[Depends(auth_admin)],
)
async def create_order(order: Order):
    return database_service.create_order(
            APP_DB,
            Order(
                contact_number = order.contact_number,
                size_description = order.size_description,
                status = order.status,
                dropoff_lat=order.dropoff_lat,
                dropoff_lng=order.dropoff_lng,
                last_updated_at=order.last_updated_at,
                dropoff_lng_amount=order.dropoff_lng,
                created_at=order.created_at,
                delivery_center=order.delivery_center,
                delivery_center_id=order.delivery_center_id,

            )
        )

@router.post(
    "/api/create_delivery_center",
    dependencies=[Depends(auth_admin)],
)
async def create_delivery_center(delivery_center: DeliveryCenter, authorization:str = Header(None)):
    username = get_username_from_token(authorization)
    return database_service.create_delivery_center(
            APP_DB,
            DeliveryCenter(
                lat=delivery_center.lat,
                lng=delivery_center.lng,
            )
            ,username
        )

#TODO
@router.put(
    "/api/update_order",
    dependencies=[Depends(auth_admin)],
)
async def update_order(order: Order):
    return database_service.update_order(order)

#TODO
@router.delete(
    "/api/delete_order/{id}",
    dependencies=[Depends(auth_admin)],
)
async def delete_order(
    id: str,
):
    return database_service.delete_order(id)

#TODO
@router.delete(
    "/api/delete_delivery_center/{id}",
    dependencies=[Depends(auth_admin)],
)
async def delete_delivery_center(
    id: str,
):
    return database_service.delete_delivery_center(id)
