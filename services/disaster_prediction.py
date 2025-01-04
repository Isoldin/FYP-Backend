import cv2
import tensorflow as tf

model = tf.saved_model.load('prediction_models/disaster_model')

def disaster_predict(image_path: str):
    img = cv2.imread(image_path)
    infer = model.signatures["serving_default"]
    result = infer(tf.constant(img))
    return result