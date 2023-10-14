from fastapi import FastAPI
from uvicorn import run
from api.router import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

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
app.include_router(router)

if __name__ == "__main__":
    run(app="main:app", host="0.0.0.0", port=8000, reload=True)