import os

import cv2
import numpy as np
import pandas as pd
import plotly.express as px
from skimage import io
import pytesseract

# settings
INPUT_WIDTH = 640
INPUT_HEIGHT = 640

# Основний шлях до вашого Django проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Шлях до папки datascience
datascience_path = os.path.join(BASE_DIR, 'datascience')

# Шлях до файлу моделі та зображення
model_path = os.path.join(datascience_path, 'best.onnx')
image_path = os.path.join(datascience_path, 'img/foto/ind2.jpeg')

# Тепер використовуємо ці шляхи
net = cv2.dnn.readNetFromONNX(model_path)
img = io.imread(image_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def get_detections(img, net):
    # 1.CONVERT IMAGE TO YOLO FORMAT
    image = img.copy()
    row, col, d = image.shape

    max_rc = max(row, col)
    input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
    input_image[0:row, 0:col] = image

    blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (INPUT_WIDTH, INPUT_HEIGHT), swapRB=True, crop=False)
    net.setInput(blob)
    preds = net.forward()
    detections = preds[0]

    return input_image, detections


def non_maximum_supression(input_image, detections):
    # center x, center y, w , h, conf, proba
    boxes = []
    confidences = []

    image_w, image_h = input_image.shape[:2]
    x_factor = image_w / INPUT_WIDTH
    y_factor = image_h / INPUT_HEIGHT

    for i in range(len(detections)):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.4:
            class_score = row[5]
            if class_score > 0.25:
                cx, cy, w, h = row[0:4]

                left = int((cx - 0.5 * w) * x_factor)
                top = int((cy - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])

                confidences.append(confidence)
                boxes.append(box)

    boxes_np = np.array(boxes).tolist()
    confidences_np = np.array(confidences).tolist()

    index = cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)

    return boxes_np, confidences_np, index


def drawings(image, boxes_np, confidences_np, index):
    for ind in index:
        x, y, w, h = boxes_np[ind]
        bb_conf = confidences_np[ind]
        conf_text = 'plate: {:.0f}%'.format(bb_conf * 100)
        license_text = extract_text(image, boxes_np[ind])

        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv2.rectangle(image, (x, y - 30), (x + w, y), (255, 0, 255), -1)
        cv2.rectangle(image, (x, y + h), (x + w, y + h + 25), (0, 0, 0), -1)

        cv2.putText(image, conf_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cv2.putText(image, license_text, (x, y + h + 27), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

    return image


# predictions flow with return result
def yolo_predictions(img, net):
    # step-1: detections
    input_image, detections = get_detections(img, net)
    # step-2: NMS
    boxes_np, confidences_np, index = non_maximum_supression(input_image, detections)
    # step-3: Drawings and text extraction
    result_img = drawings(input_image, boxes_np, confidences_np, index)  # Make sure you use input_image here if needed
    recognized_text = extract_text(result_img, boxes_np[index[0]]) if index.size > 0  else "No number recognized"
    return result_img, recognized_text


# extrating text
def extract_text(image, bbox):
    x, y, w, h = bbox
    roi = image[y:y + h, x:x + w]

    if 0 in roi.shape:
        return 'no number'

    else:
        text = pytesseract.image_to_string(roi)
        text = text.strip()
        return text


# test
results = yolo_predictions(img, net)
"""
fig = px.imshow(results)
fig.update_layout(width=800, height=700, margin=dict(l=10, r=10, b=10, t=10))
fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig.show()
"""