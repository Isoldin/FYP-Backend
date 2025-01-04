from pathlib import Path

import cv2
from fastapi import APIRouter, UploadFile, File, HTTPException
from ultralytics import YOLO
from services.detect_human import detect_and_plot_human
from starlette import status
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"]
)

model = YOLO('prediction_models/human_detection_model/yolov9c.pt')

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = BASE_DIR / "prediction_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/detect_human", status_code=status.HTTP_200_OK)
async def detect_human(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type!")

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = detect_and_plot_human(str(file_path))

    result_path = OUTPUT_DIR / file.filename

    cv2.imwrite(str(result_path), result)

    return FileResponse(result_path, media_type="image/png")