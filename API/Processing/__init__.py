import cv2 as cv
import numpy as np

from .utils import getMeanSize, getMeanDistance
from .segmentation import getRects, floodfill8D
from .textSeparator import orderChars, separeLines, separeWords, wordCorrector

def precessText(img, thresh = 125, erode = (0, 0), dilate = (0, 0), floodfill_algorithm = segmentation.floodfill8D):
    binarized = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binarized = cv.threshold(binarized, thresh, 255, cv.THRESH_BINARY)
    
    if erode != (0, 0):
        binarized = cv.erode(binarized, np.ones(erode))
    if dilate != (0, 0):
        binarized = cv.dilate(binarized, np.ones(dilate))
        
    rects = getRects(binarized, floodfill8D)
    print(len(rects))
    mean_height, mean_width = getMeanSize(rects)
    text = orderChars(rects)
    text = separeLines(text, mean_height)
    mean_distance = getMeanDistance(text)
    text = [separeWords(text[i], mean_distance) for i in range(len(text))]
    for line in text:
        for word in line:
            wordCorrector(word)
            
    return text

def indexToAscii(index):
    values = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '97', '98', '99']
    return values[index]