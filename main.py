from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine
from typing import Annotated
from starlette import status
from routes import auth, pagination

app = FastAPI()
app.include_router(auth.router)
app.include_router(pagination.router)

models.Base.metadata.create_all(engine)

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def root(user: user_dependency):
    if user is None or user.get('role') != "client":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return {"User": user}
