import os
import cv2 as cv
import numpy as np

def SaveImage(path, file, img):
    if not os.path.exists(path):
        os.makedirs(path)
    cv.imwrite(f'{path}/{file}', img)
    
def Rects2Rect(rects):
    xi, yi = rects[0][0]
    xf, yf = rects[0][1]
    
    for rect in rects:
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        
        xi = min(xi, x1)
        yi = min(yi, y1)
        xf = max(xf, x2)
        yf = max(yf, y2)
    return ((xi, yi), (xf, yf))

def GetTotalFiles(path):
    count = 0
    for file in os.listdir(path):
        if os.path.isfile(f'{path}/{file}'):
            count += 1
        else:
            count += GetTotalFiles(f'{path}/{file}')
    return count

def GetTotalFolders(path):
    count = 0
    for dir in os.listdir(path):
        if os.path.isdir(f'{path}/{dir}'):
            count += 1
    return count

def isBinarized(img):
    unique_pixels = np.unique(img)
    if len(unique_pixels) == 2:
        hist = cv.calcHist([img], [0], None, [256], [0, 256])
        peaks = np.where(hist > 0)[0]
        if len(peaks) == 2:
            return True
    return False

def resize(img, size):
    heigth, width = img.shape[:2]
    nwidth, nheigth = size
    
    new_img = np.ones((nheigth, nwidth, 3), dtype=np.uint8) * 255
    
    scale = min(nwidth/width, nheigth/heigth)
    sheight = int(heigth * scale)
    swidth = int(width * scale)
    
    y = (nheigth - sheight) // 2
    x = (nwidth - swidth) // 2
    
    img = cv.resize(img, (swidth, sheight))
    
    new_img[y:y+sheight, x:x+swidth] = img
    return new_img