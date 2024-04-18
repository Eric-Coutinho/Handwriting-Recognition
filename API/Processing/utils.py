import cv2 as cv
import numpy as np

def cutImage(img, rect):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    
    return img[y1:y2, x1:x2]

def resize(img, size):
    print(img.shape)
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

def rectCenter(rect):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    
    x = int((x1 + x2) / 2)
    y = int((y1 + y2) / 2)
    
    return (x, y)

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

def getMeanSize(rects):
    mean_width = 0
    mean_height = 0
    for char in rects:
        mean_width += char[1][0] - char[0][0]
        mean_height += char[1][1] - char[0][1]
    mean_width /= len(rects)
    mean_height /= len(rects)
    
    return (mean_height, mean_width)

def getMeanDistance(lines):
    distance = 0
    spaces = 0
    for line in lines:
        for i in range(len(line)):
            if i < 1 <= 0:
                continue
        
            spaces += 1
            distance += max(0, line[i][0][0] - line[i - 1][1][0])
    return distance / spaces

def asciiToChar(ascii_value):
    if isinstance(ascii_value, int):
        char_value = chr(ascii_value)
        return char_value
    else:
        return ""