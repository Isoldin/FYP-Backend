from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UploadedImagesPaginationRequest(BaseModel):
    skip: int = 0
    limit: int = 0
    search_user_id: Optional[int] = None
    sort_by: str = "uploaded_date"
    sort_order: str = "desc"

class UploadedImagesPaginationResponse(BaseModel):
    image_id: int
    type_of_disaster: str
    uploaded_date: datetime

class UploadImageRequest(BaseModel):
    img_name: str
    geolocation: dict
    type_of_disaster: str

class UploadImageDetailsResponse(BaseModel):
    image_id: int
    img_name: str
    geolocation: dict
    type_of_disaster: str
    uploaded_by: str
    uploaded_date: datetime