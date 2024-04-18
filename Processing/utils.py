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

def RectContains(rect, coord):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    x, y = coord
    
    if x >= x1 and x <= x2 and y >= y1 and y <= y2:
        return True
    return False

def RectsContains(rects, coord):
    for rect in rects:
        if RectContains(rect, coord):
            return True
    return False

def getBackColors(img, rects):
    covered_area = set()
    for rect in rects:
        (x1, y1), (x2, y2) = rect
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                covered_area.add((x, y))

    unique_colors = {}
    for y in range(len(img)):
        row = img[y]
        for x in range(len(row)):
            if (x, y) not in covered_area:
                b, g, r = row[x]
                unique_colors[(b, g, r)] = True

    return list(unique_colors.keys())
            
def binarizeByColors(img, colors):
    h, w = img.shape[:2]
    
    # Cria uma matriz binária indicando se cada pixel está na lista de cores
    color_mask = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            if tuple(img[y][x]) in colors:
                color_mask[y][x] = True
    
    # Aplica a máscara de cores para binarizar a imagem
    for y in range(h):
        for x in range(w):
            if color_mask[y][x]:
                img[y][x] = (255, 255, 255)
            else:
                img[y][x] = (0, 0, 0)