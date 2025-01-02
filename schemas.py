from typing import Optional
from pydantic import BaseModel, Field
from models import Users

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPaginationRequest(BaseModel):
    skip: int = 0
    limit: int = 10
    search_username: Optional[str] = None
    search_role: Optional[str] = None
    sort_by: str = "user_id"
    sort_order: str = "asc"

class UserPaginationResponse(BaseModel):
    user_id: int
    username: str
    role: str
