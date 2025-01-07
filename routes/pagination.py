from fastapi import Depends, APIRouter
from typing import List, Annotated, Optional
from models import UploadedImages
from schemas import UploadedImagesPaginationResponse, UploadedImagesPaginationRequest
from starlette import status
from sqlalchemy import asc, desc
from dependencies import db_dependency

router = APIRouter(
    prefix="/pagination",
    tags=["pagination"]
)

@router.get("/uploaded_image", response_model=List[UploadedImagesPaginationResponse], status_code=status.HTTP_200_OK)
def paginate_uploads(
    request: Annotated[UploadedImagesPaginationRequest, Depends()],
    db: db_dependency
):
    query = db.query(UploadedImages)
    if request.search_user_id:
        query = query.filter(UploadedImages.uploaded_by==request.search_user_id)

    # Apply sorting
    if request.sort_order == "asc":
        query = query.order_by(asc(getattr(UploadedImages, request.sort_by)))
    else:
        query = query.order_by(desc(getattr(UploadedImages, request.sort_by)))

    # Apply pagination
    if request.limit == 0:
        uploaded_images = query.all()
    else:
        uploaded_images = query.offset(request.skip).limit(request.limit).all()

    return uploaded_images
