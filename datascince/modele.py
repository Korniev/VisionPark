import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Завантаження навченої моделі з файлу model.h5
loaded_model = load_model('model.h5')

# Зчитуємо зображення номерного знака
plate_image = cv2.imread(r'\img\foto\eu1.jpg')
plate_image = cv2.resize(plate_image, (32, 32))
plate_image = np.array(plate_image) / 255.0  # Нормалізація

# Отримання прогнозу моделі для зображення номерного знака
plate_text_prob = loaded_model.predict(np.expand_dims(plate_image, axis=0))

# Отримання індексу максимального значення
max_prob_index = np.argmax(plate_text_prob)

# Перевірка, чи індекс належить допустимим класам (цифри та літери)
if max_prob_index >= 0 and max_prob_index <= 35:
    if max_prob_index <= 9:
        predicted_class = str(max_prob_index)  # Цифра
    else:
        predicted_class = chr(ord('A') + (max_prob_index - 10))  # Літера
else:
    predicted_class = 'Неможливо розпізнати'

print('Прогнозована мітка класу для номерного знака:', predicted_class)
