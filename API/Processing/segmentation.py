import cv2 as cv
import numpy as np

def floodfill4D(img, x, y):
    x0 = x
    xf = x
    y0 = y
    yf = y
    
    queue = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]
    
    while len(queue) > 0:
        x, y = queue.pop()
        
        if y < 0 or y >= len(img):
            continue
        
        row = img[y]
        
        if x < 0 or x >= len(row):
            continue
            
        pixel = row[x]
        
        if pixel == 255:
            continue
        img[y][x] = 255
        
        x0 = min(x0, x)
        xf = max(xf, x)
        y0 = min(y0, y)
        yf = max(yf, y)
        
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))
        
    return ((x0, y0), (xf, yf))

def floodfill8D(img, x, y):
    x0 = x
    xf = x
    y0 = y
    yf = y
    
    queue = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1)
    ]
    
    while len(queue) > 0:
        x, y = queue.pop()
        
        if y < 0 or y >= len(img):
            continue
        
        row = img[y]
        
        if x < 0 or x >= len(row):
            continue
            
        pixel = row[x]
        
        if pixel == 255:
            continue
        img[y][x] = 255
        
        x0 = min(x0, x)
        xf = max(xf, x)
        y0 = min(y0, y)
        yf = max(yf, y)
        
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))
        queue.append((x + 1, y + 1))
        queue.append((x - 1, y - 1))
        queue.append((x + 1, y - 1))
        queue.append((x - 1, y + 1))
        
    return ((x0, y0), (xf, yf))

def getRects(org, algorithm = floodfill4D):
    img = org.copy()
        
    rects = []
    for i in range(len(img)):
        row = img[i]
        for k in range(len(row)):
            if row[k] == 0:
                rects.append(algorithm(img, k, i))
    return rects

def cutImage(img, rect):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    
    return img[y1:y2, x1:x2]