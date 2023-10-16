from typing import List
from starlette import status
from services import database_service
from config.config import ConfigClass
from starlette.requests import Request
from clients.db_client import DBclient
from services import authentication_service
from starlette.responses import JSONResponse
from utils.utils import get_username_from_token
from services.authentication_service import auth_admin, auth_user
from fastapi import Body, Depends, HTTPException, APIRouter, Header
from api.input_objects_schemas import User,Order, DeliveryCenter, UpdateOrderModel

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
    db_client = DBclient(ConfigClass.SQL_CONNECTION_STRING)
    token = authentication_service.login(db_client, User(username=username, password=password))
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
    delivery_centers: List[DeliveryCenter] | None =\
        database_service.list_delivery_centers(APP_DB, id=id)
    if not delivery_centers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DELIVERY_CENTER_DOES_NOT_EXIST")
    return JSONResponse(delivery_centers, status_code=status.HTTP_201_CREATED)

@router.get(
    "/api/authenticated/delivery_centers",
    dependencies=[Depends(auth_admin)],
    response_model=DeliveryCenter
)
async def get_delivery_center(id: str = None,authorization:str = Header(None)):
    username = get_username_from_token(authorization)
    args = [APP_DB,username,id]
    response= \
        database_service.list_delivery_centers_for_authenticated_user(*args)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DELIVERY_CENTER_DOES_NOT_EXIST")
    return JSONResponse(response, status_code=status.HTTP_201_CREATED)

@router.post(
    "/api/create_order",
    dependencies=[Depends(auth_admin)],
)
async def create_order(order: Order, authorization= Header(None)):
    username = get_username_from_token(authorization)
    response = \
        database_service.create_order(db_client=APP_DB,username=username, order=order)
    if not response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(response, status_code=status.HTTP_201_CREATED)

@router.post(
    "/api/create_delivery_center",
    dependencies=[Depends(auth_admin)],
)
async def create_delivery_center(delivery_center: DeliveryCenter, authorization:str = Header(None)):
    username = get_username_from_token(authorization)
    response = database_service.create_delivery_center(APP_DB,delivery_center,username)
    if not response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(response, status_code=status.HTTP_201_CREATED)

@router.put(
    "/api/update_order/{order_id}",
    dependencies=[Depends(auth_admin)],
    response_model=Order
)
async def update_order(order_id: str, update_data: UpdateOrderModel):
    response = database_service.update_order(APP_DB, order_id, update_data)
    if not response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(response, status_code=status.HTTP_201_CREATED)

#TODO
# @router.delete(
#     "/api/delete_order/{id}",
#     dependencies=[Depends(auth_admin)],
# )
# async def delete_order(
#     id: str,
# ):
#     return database_service.delete_order(id)

#TODO
# @router.delete(
#     "/api/delete_delivery_center/{id}",
#     dependencies=[Depends(auth_admin)],
# )
# async def delete_delivery_center(
#     id: str,
# ):
#     return database_service.delete_delivery_center(id)
