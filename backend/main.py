from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from uvicorn import run

from backend.consts import REQUESTS_AUTH_TOKEN, SQL_CONNECTION_STRING
from backend.report import PartialReport, Report, User
from backend.reports_db import ReportsDB
from backend.sql_reports_db import SqlReportsDB

app = FastAPI()
REPORTS_DB: ReportsDB = SqlReportsDB(SQL_CONNECTION_STRING)

origins = [
    "*",
    "http://localhost:4200/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def auth_user(request: Request):
    auth_token = request.headers.get(REQUESTS_AUTH_TOKEN)
    if not (auth_token and REPORTS_DB.auth_user(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

async def auth_admin(request: Request):
    auth_token = request.headers.get(REQUESTS_AUTH_TOKEN)
    if not (auth_token and REPORTS_DB.auth_admin(auth_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

@app.post("/api/login", response_model=str)
async def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
):
    token = REPORTS_DB.login(User(username=username, password=password))
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    return token

@app.get(
    "/api/reports/all",
    dependencies=[Depends(auth_user)],
    response_model=List[Report],
)
async def get_reports():
    return REPORTS_DB.get_reports()

@app.post(
    "/api/create",
    dependencies=[Depends(auth_admin)],
)
async def create_report(report: PartialReport):
    return REPORTS_DB.create(
            PartialReport(
                description=report.description,
                lat=report.lat,
                lng=report.lng,
                type=report.type,
                report_amount=report.report_amount
            )
        )

@app.put(
    "/api/update",
    dependencies=[Depends(auth_admin)],
)
async def update_reports(report: Report):
    return REPORTS_DB.update(report)

@app.delete(
    "/api/delete/{id}",
    dependencies=[Depends(auth_admin)],
)
async def delete_report(
    id: str,
):
    return REPORTS_DB.delete(id)

if __name__ == "__main__":
    run(app="main:app", host="0.0.0.0", port=8000, reload=True)
