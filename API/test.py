import Processing as pcs
import cv2 as cv
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("./989-995.keras")
img = cv.imread("./screenshot.png")
text = pcs.precessText(img)

result = ""
for line in text:
    for word in line:
        for char in word:
            if char[0][0] == char[1][0] or char[0][1] == char[1][1]:
                continue
            image = pcs.utils.cutImage(img, char)
            image = pcs.utils.resize(image, (128, 128))
            data = np.array([image])
            predict = model.predict(data)
            result += pcs.utils.asciiToChar(pcs.indexToAscii(np.argmax(predict)))
        result += " "
    result += "\n"
print(result)