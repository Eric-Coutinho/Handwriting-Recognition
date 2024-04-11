import os
import cv2 as cv

from utils import SaveImage, Rects2Rect
from segmentation import getRects, cutImage

folder = "../Img"

for dir in os.listdir(folder):
    for file in os.listdir(f"{folder}/{dir}"):
        img_path = f"{folder}/{dir}/{file}"
        img = cv.imread(img_path)
        
        rects = getRects(img)
        if len(rects) > 1:
            print(img_path)
            
        cropped = cutImage(img, Rects2Rect(rects))
        SaveImage(f"./Img/{dir}", file, cropped)
            
        