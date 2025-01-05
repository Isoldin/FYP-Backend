import cv2
import numpy as np
import keras

model = keras.models.load_model('prediction_models/disaster_model/final_model.keras')

CLASS_LABELS = {
    0: 'Damaged_Infrastructure',
    1: 'Fire_Disaster',
    2: 'Human_Damage',
    3: 'Land_Disaster',
    4: 'Non_Damage',
    5: 'Water_Disaster'
}

def get_model_summary():
    return model.summary()

def disaster_predict(image_path: str):
    img = cv2.imread(image_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR (OpenCV) to RGB
    img = cv2.resize(img, (150, 150))  # Resize to the required size
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    # Convert predictions to a JSON-compatible format
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    predicted_class = CLASS_LABELS[predicted_class_index]
    probabilities = {CLASS_LABELS[i]: float(prediction[0][i]) for i in range(len(CLASS_LABELS))}

    return {"predicted_class": predicted_class, "probabilities": probabilities}
