import cv2 as cv

from segmentation import *
from utils import *

img = cv.imread('./test1.jpg')

max_width = 1280
max_height = 720
height, width = img.shape[:2]
if width > max_width or height > max_height:
    scale = min(max_width / width, max_height / height)
    img = cv.resize(img, (int(width * scale), int(height * scale)))
copy = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, copy = cv.threshold(copy, 150, 255, cv.THRESH_BINARY)

copy = cv.erode(copy, np.ones((5, 5)))
copy = cv.dilate(copy, np.ones((7, 7)))

rects = getRects(copy, floodfill8D)

def rectCenter(rect):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    
    x = int((x1 + x2) / 2)
    y = int((y1 + y2) / 2)
    
    return (x, y)

def compareTo(rect, reference):
    x, y = rectCenter(rect)
    
    x1, y1 = reference[0]
    x2, y2 = reference[1]
    rx, ry = rectCenter(reference)
    
    if y > y1 and x > rx:
        return 1
    
    if y > y1 and x < rx:
        return -1
    
    if y < ry:
        return -1
    
    if y > ry:
        return 1
    
    return 0

def orderInsert(list, item):
    index = 0
    while index < len(list) and compareTo(list[index], item) < 0:
        index += 1
    list.insert(index, item)

mark = img.copy()
for rect in rects:
    mark = cv.rectangle(mark, rect[0], rect[1], (0, 255, 0), 2)
    
text = []
for rect in rects:
    x, y = rectCenter(rect)
    
    mark = cv.circle(mark, (x, y), 3, (255, 0, 0), thickness=-1)
    
    if len(text) == 0:
        text.append(rect)
        continue
    orderInsert(text, rect)
    
scale = 150 / len(text)
lines = 0
for char in range(len(text) - 1):
    start = rectCenter(text[char])
    end = rectCenter(text[char + 1])
    
    cv.line(mark, start, end, (50, 50, 255 - int(scale * lines)), 2)
    lines += 1
    
cv.imshow('image', mark)
cv.waitKey(0)    

# for rect in rects:
#     mark = img.copy()
#     mark = cv.rectangle(mark, rect[0], rect[1], (0, 255, 0), 2)
#     cv.imshow('image', mark)
#     cv.waitKey(0)