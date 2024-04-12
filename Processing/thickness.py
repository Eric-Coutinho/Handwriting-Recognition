import random
import numpy as np
import cv2 as cv

from segmentation import getRects, cutImage
from utils import Rects2Rect

def thicknessImg(img):
    rand = random.randint(-1, 3)
    size = random.randint(0, 30)
    
    img = resize(img, 1.5)
    if (rand < 1):
        img = cv.erode(img, np.ones((size, size)))
    else:
        img = cv.dilate(img, np.ones((size, size)))
        
    rects = getRects(img)
    img = cutImage(img, Rects2Rect(rects))

    return img

def resize(img, scale):
    heigth, width = img.shape[:2]
    nheigth = int(heigth * scale)
    nwidth = int(width * scale)
    
    new_img = np.ones((nheigth, nwidth, 3), dtype=np.uint8) * 255
    
    y = (nheigth - heigth) // 2
    x = (nwidth - width) // 2
    
    new_img[y:y+heigth, x:x+width] = img
    return new_img


if __name__ == "__main__":
    img = cv.imread('./Img/115/011.png')
    
    while True:
        copy = img.copy()
        copy = thicknessImg(copy)
        
        cv.imshow("Image", copy)
        cv.waitKey(0)
    