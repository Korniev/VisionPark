import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from tensorflow.keras.models import load_model

model = load_model('model.keras')

img = cv2.imread(r'./img/foto/eu4.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(gray, cmap='gray')
plt.show()

bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(bfilter, 30, 200)
plt.imshow(edged, cmap='gray')
plt.show()

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break

mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
plt.show()

(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
plt.show()


# перехід до розпізнавання кожного символу

# Бінаризація та морфологічне очищення
kernel = np.ones((3,3), np.uint8)
# binary_image = cv2.adaptiveThreshold(cropped_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 2)
_, binary_image = cv2.threshold(cropped_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=1)
binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=1)
plt.imshow(binary_image, cmap='gray')
plt.show()


# Виявлення контурів символів
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
symbols = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    margin = 5
    if w*h > 10:
        extended_x = max(x - margin, 0)
        extended_y = max(y - margin, 0)
        extended_w = min(w + 2*margin, binary_image.shape[1] - extended_x)
        extended_h = min(h + 2*margin, binary_image.shape[0] - extended_y)
        symbol = cropped_image[extended_y:extended_y + extended_h, extended_x:extended_x + extended_w]
        if symbol.size > 0:
            symbols.append(symbol)
            plt.imshow(symbol, cmap='gray')
            plt.show()

# Підготовка символів до класифікації
prepared_symbols = [cv2.resize(symbol, (32, 32)) for symbol in symbols if symbol.size > 0]
prepared_symbols = np.array(prepared_symbols) / 255.0
prepared_symbols = np.stack([prepared_symbols]*3, axis=-1)
prepared_symbols = prepared_symbols.reshape(-1, 32, 32, 3)

# Завантаження назв класів
data_dir = r'img/train'
classes = os.listdir(data_dir)

# Класифікація символів
if len(prepared_symbols) > 0:
    predictions = model.predict(prepared_symbols)
    predicted_classes = np.argmax(predictions, axis=1)
    predicted_class_labels = [classes[idx] for idx in predicted_classes]
    print("Classified symbols:", predicted_class_labels)
else:
    print("No ones symbols found.")