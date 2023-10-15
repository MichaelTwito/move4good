from repositories.db import DBclient
from fastapi import Body, Depends, HTTPException, APIRouter, Header
from starlette import status
from typing import List
from starlette.requests import Request
from services import database_service
from config.config import ConfigClass
from repositories.enteties import User,Order, DeliveryCenter, UpdateOrderModel
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
    "/api/delivery_centers",
    response_model=List[DeliveryCenter],
)
async def list_delivery_centers(id: str = None):
    return database_service.list_delivery_centers(APP_DB, id=id)


@router.get(
    "/api/delivery_center",
    dependencies=[Depends(auth_admin)],
    response_model=DeliveryCenter
)
async def get_delivery_center(authorization:str = Header(None)):
    username = get_username_from_token(authorization)
    delivery_center_id = database_service.get_delivery_center_id_for_username(APP_DB,username)
    response =\
          database_service.get_delivery_center(APP_DB, delivery_center_id)
    if not delivery_center_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DELIVERY_CENTER_DOES_NOT_EXIST")
    return response

@router.post(
    "/api/create_order",
    dependencies=[Depends(auth_admin)],
)
async def create_order(order: Order):
    return database_service.create_order(db_client=APP_DB,order=order)

@router.post(
    "/api/create_delivery_center",
    dependencies=[Depends(auth_admin)],
)
async def create_delivery_center(delivery_center: DeliveryCenter, authorization:str = Header(None)):
    username = get_username_from_token(authorization)
    return database_service.create_delivery_center(
            APP_DB,
            DeliveryCenter(
                name=delivery_center.name,
                address=delivery_center.address,
                lat=delivery_center.lat,
                lng=delivery_center.lng
            )
            ,username
        )

@router.put(
    "/api/update_order/{order_id}",
    dependencies=[Depends(auth_admin)],
    response_model=Order
)
async def update_order(order_id: str, update_data: UpdateOrderModel):
    return database_service.update_order(APP_DB, order_id, update_data)

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
