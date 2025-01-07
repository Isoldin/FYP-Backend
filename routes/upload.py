import uuid
from datetime import datetime, timezone
from pathlib import Path
from starlette import status
from fastapi import APIRouter, File, UploadFile, HTTPException
from schemas import UploadImageRequest, UploadImageDetailsResponse
from dependencies import db_dependency, user_dependency
from models import UploadedImages, Users

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type!")

    #generating a unique name to avoid overwriting
    new_file_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = UPLOAD_DIR / new_file_name

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"file_name": new_file_name}

@router.post('/save_to_db', status_code=status.HTTP_201_CREATED)
async def save_to_db(request: UploadImageRequest, user:user_dependency, db: db_dependency):

    upload_image_model = UploadedImages(
        img_name=request.img_name,
        geolocation=request.geolocation,
        type_of_disaster=request.type_of_disaster,
        uploaded_by=user['id'],
        uploaded_date=datetime.now(timezone.utc),
    )

    db.add(upload_image_model)
    db.commit()
    db.refresh(upload_image_model)

    return upload_image_model

@router.get("/detail", status_code=status.HTTP_200_OK, response_model=UploadImageDetailsResponse)
async def get_record_details(id: int, db: db_dependency):
    detail=db.query(UploadedImages).filter_by(image_id=id).first()

    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found!")

    uploader_user = db.query(Users).filter_by(user_id=detail.uploaded_by).first()
    uploader_username = uploader_user.username

    detail_response = {
        "image_id": detail.image_id,
        "img_name": detail.img_name,
        "geolocation": detail.geolocation,
        "type_of_disaster": detail.type_of_disaster,
        "uploaded_by": uploader_username,
        "uploaded_date": detail.uploaded_date,
    }
    return detail_response