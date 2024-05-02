import cv2
import numpy as np
from tensorflow.keras.models import load_model


model = load_model(r'C:\Users\chorn\VisionPark\datascince\img\model.h5')

# Шлях до вхідного зображення автомобіля
input_image_path = r'C:\Users\chorn\VisionPark\datascince\img\foto\eu1.jpg'

# Завантаження вхідного зображення автомобіля
input_image = cv2.imread(input_image_path)

# Визначення області номерного знаку на зображенні автомобіля (припустимо, що ви вже маєте цю область)
license_plate_region = input_image[y1:y2, x1:x2]  # Замініть x1, y1, x2, y2 координатами області номерного знаку

# Зміна розміру та нормалізація зображення номерного знаку
license_plate_resized = cv2.resize(license_plate_region, (32, 32)) / 255.0

# Передача зображення через модель для розпізнавання номерного знаку
prediction = model.predict(np.array([license_plate_resized]))

# Отримання розпізнаного тексту (припустимо, що маємо класи 'A', 'B', 'C' ... '9' для розпізнавання)
classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
predicted_class_idx = np.argmax(prediction)
recognized_text = classes[predicted_class_idx]

print("Розпізнаний текст з номерного знаку:", recognized_text)
