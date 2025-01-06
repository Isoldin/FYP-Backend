from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Annotated
from models import Users
from schemas import UserPaginationResponse, UserPaginationRequest
from starlette import status
from sqlalchemy import asc, desc
from dependencies import db_dependency

router = APIRouter(
    prefix="/pagination",
    tags=["pagination"]
)

@router.get("/users", response_model=List[UserPaginationResponse], status_code=status.HTTP_200_OK)
def get_users(
    request: Annotated[UserPaginationRequest, Depends()],
    db: db_dependency
):
    query = db.query(Users)
    if request.search_username:
        query = query.filter(Users.username.ilike(f"%{request.search_username}%"))
    if request.search_role:
        query = query.filter(Users.role.ilike(f"%{request.search_role}%"))

    # Apply sorting
    if request.sort_order == "asc":
        query = query.order_by(asc(getattr(Users, request.sort_by)))
    else:
        query = query.order_by(desc(getattr(Users, request.sort_by)))

    # Apply pagination
    users = query.offset(request.skip).limit(request.limit).all()
    return users

