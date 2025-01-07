import os
from pathlib import Path
import cv2
from ultralytics import YOLO

model = YOLO('prediction_models/human_detection_model/best.pt')

def detect_and_plot_human(image_path: str):
    img = cv2.imread(image_path)
    results = model(img)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf.cpu().numpy())

            #logic to plot the detected human
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
            label = f'{conf:.2f}'
            cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0), 1)

    return img