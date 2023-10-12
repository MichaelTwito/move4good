from repositories.db import DBclient
from fastapi import Body, Depends, HTTPException, APIRouter
from starlette import status
from typing import List
from starlette.requests import Request
from services import authentication_service,database_service
from config.config import ConfigClass
from repositories.enteties import User,Order, DeliveryCenter

router = APIRouter()
APP_DB= DBclient(ConfigClass.SQL_CONNECTION_STRING)

async def auth_user(request: Request):
    auth_token = request.headers.get(ConfigClass.REQUESTS_AUTH_TOKEN)
    if not (auth_token and APP_DB.auth_user(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

async def auth_admin(request: Request):
    auth_token = request.headers.get(ConfigClass.REQUESTS_AUTH_TOKEN)
    if not (auth_token and authentication_service.auth_admin(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

@router.post("/api/login", response_model=str)
async def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
):
    print(dir(APP_DB))
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
    return APP_DB.get_orders()

@router.post(
    "/api/create_order",
    dependencies=[Depends(auth_admin)],
)
#TODO
async def create_order(order: Order):
    return database_service.create_order(
            Order(
                contact_number = order.contact_number,
                size_description = order.size_description,
                status = 1,
                dropoff_lat=order.dropoff_lat,
                dropoff_lng_amount=order.dropoff_lng
            )
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



@router.post(
    "/api/create_delivery_center",
    dependencies=[Depends(auth_admin)],
)
#TODO
async def create_delivery_center(delivery_center: DeliveryCenter):
    return database_service.create_delivery_center(
            APP_DB,
            DeliveryCenter(
                lat=delivery_center.lat,
                lng=delivery_center.lng,
            )
        )

#TODO
@router.delete(
    "/api/delete_delivery_center/{id}",
    dependencies=[Depends(auth_admin)],
)
async def delete_delivery_center(
    id: str,
):
    return database_service.delete_delivery_center(id)
