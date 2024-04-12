import random
import numpy as np
import cv2 as cv

def thicknessImg(img):
    rand = random.randint(-1, 3)
    size = random.randint(0, 50)
    
    if (rand < 1):
        img = cv.erode(img, np.ones((size, size)))
    else:
        img = cv.dilate(img, np.ones((size, size)))

    return img

def resize(img, scale):
    altura, largura = img.shape[:2]
    return cv.resize(img, (largura * scale, altura * scale))