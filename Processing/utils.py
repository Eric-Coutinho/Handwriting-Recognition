import os
import cv2 as cv

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