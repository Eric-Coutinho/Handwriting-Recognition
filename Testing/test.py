import tensorflow as tf
import numpy as np
import cv2 as cv
import os

def ascii_to_char(ascii_value):
    if isinstance(ascii_value, int):
        char_value = chr(ascii_value)
        return char_value
    else:
        return "Input must be an integer representing ASCII value"

model = tf.keras.models.load_model("Testing/98-99.keras")

image = cv.imread("Testing/ImgTest/003.png")

resized_image = cv.resize(image, (128, 128))

image_list = []
image_list.append(resized_image)

data = np.array(image_list)

result = model.predict(data)

maxIndex = np.argmax(result)

folders = os.listdir("./Img")
print(result)
print("Maior Index:", folders[maxIndex])

value = int(folders[maxIndex])
print("Character:", ascii_to_char(value))
