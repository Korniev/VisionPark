import cv2
import numpy as np
from tensorflow.keras.models import load_model

loaded_model = load_model('model.h5')

plate_image = cv2.imread(r'\img\foto\eu1.jpg')
plate_image = cv2.resize(plate_image, (32, 32))
plate_image = np.array(plate_image) / 255.0

plate_text_prob = loaded_model.predict(np.expand_dims(plate_image, axis=0))

max_prob_index = np.argmax(plate_text_prob)

if max_prob_index >= 0 and max_prob_index <= 35:
    if max_prob_index <= 9:
        predicted_class = str(max_prob_index)
    else:
        predicted_class = chr(ord('A') + (max_prob_index - 10))
else:
    predicted_class = 'It is impossible to recognize'

print('Predicted class label for license plate:', predicted_class)
