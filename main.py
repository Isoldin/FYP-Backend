from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import models
from database import engine
from starlette import status
from routes import auth, pagination, upload, prediction
from dependencies import user_dependency

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pagination.router)
app.include_router(prediction.router)
app.include_router(upload.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/prediction_results", StaticFiles(directory="prediction_results"), name="prediction_results")