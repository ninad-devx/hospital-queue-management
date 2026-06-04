from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.department import router as department_router
from routes.token import router as token_router

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(department_router)
app.include_router(token_router)
