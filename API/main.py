import Processing as pcs
from flask import Flask, request, jsonify
import cv2 as cv
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("./989-995.keras")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def Predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    text = pcs.precessText(img)
    
    result = ""
    for line in text:
        for word in line:
            for char in word:
                image = pcs.utils.cutImage(img, char)
                image = pcs.utils.resize(image, (128, 128))
                data = np.array([image])
                predict = model.predict(data)
                result += pcs.utils.asciiToChar(pcs.indexToAscii(np.argmax(predict)))
            result += " "
        result += "\n"
    
    return jsonify({'text': result})
    
if __name__ == '__main__':
    app.run(debug=True)