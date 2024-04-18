import tensorflow as tf
import numpy as np
import cv2 as cv
import os

import segmentation, utils

def ascii_to_char(ascii_value):
    if isinstance(ascii_value, int):
        char_value = chr(ascii_value)
        return char_value
    else:
        return "Input must be an integer representing ASCII value"

# model = tf.keras.models.load_model("Processing/989-995.keras")
model = tf.keras.models.load_model("Processing/98-99.keras")

image = cv.imread("Processing/screenshot.png")

rects = segmentation.getRects(image)

resized_image = segmentation.cutImage(image, utils.Rects2Rect(rects))
resized_image = utils.resize(resized_image, (128, 128))

image_list = []
image_list.append(resized_image)

data = np.array(image_list)

result = model.predict(data)

print(result.shape)

maxIndex = np.argmax(result)

folders = os.listdir("./Img")
print(result)
print("Maior Index:", folders[maxIndex])

value = int(folders[maxIndex])

print("Character:", ascii_to_char(value))

