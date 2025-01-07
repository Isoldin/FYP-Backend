from pathlib import Path
import cv2
from fastapi import APIRouter, UploadFile, File, HTTPException
from ultralytics import YOLO
from services.detect_human import detect_and_plot_human
from services.disaster_prediction import disaster_predict, get_model_summary
from starlette import status
import os

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
async def detect_human(img_name: str):
    image_path = UPLOAD_DIR / img_name
    result = detect_and_plot_human(str(image_path))
    result_path = OUTPUT_DIR / img_name
    cv2.imwrite(str(result_path), result)
    return {'result_path': str(img_name)}

@router.post("/predict_disaster", status_code=status.HTTP_200_OK)
async def predict_disaster(img_name: str):
    image_path = UPLOAD_DIR / img_name
    result = disaster_predict(str(image_path))
    return result
