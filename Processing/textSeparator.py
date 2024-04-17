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
binarized = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, binarized = cv.threshold(binarized, 150, 255, cv.THRESH_BINARY)

binarized = cv.erode(binarized, np.ones((5, 5)))
binarized = cv.dilate(binarized, np.ones((7, 7)))

rects = getRects(binarized, floodfill8D)

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
    
def line_distance(line1, line2):
    _, y1 = line1[0]
    _, y2 = line2[0]
    return abs(y1 - y2)
    
def getLines(rects, mean_height):
    lines_bases = []
    lines = []
    for rect in rects:
        height = rect[1][1] - rect[0][1]
        base = rect[1][1] - (height / 2) if height > mean_height * 1.75 else rect[1][1]
        new_line = True
        for i in range(len(lines)):
            x1, y1 = lines[i][0]
            x2, y2 = lines[i][1]
            
            y = (y1 + y2) / 2
            if abs(y - base) <= mean_height:
                new_line = False
                lines_bases[i].append(base)
                mean = sum(lines_bases[i]) / len(lines_bases[i])
                lines[i] = ((int(min(x1, rect[0][0])), int(mean)), (int(max(x2, rect[1][0])), int(mean)))
        
        if new_line:
            lines.append(((rect[0][0], base), (rect[1][0], base)))
            lines_bases.append([base])
                
    merged_lines = []
    merged_bases = []
    merged_indices = set()
    for i in range(len(lines)):
        if i not in merged_indices:
            current_line = lines[i]
            current_base = lines_bases[i]
            for j in range(i + 1, len(lines)):
                if j not in merged_indices:
                    if line_distance(current_line, lines[j]) <= mean_height / 2:
                        merged_line = ((min(current_line[0][0], lines[j][0][0]), current_line[0][1]), (max(current_line[1][0], lines[j][1][0]), current_line[1][1]))
                        merged_base = current_base + lines_bases[j]
                        merged_mean = sum(merged_base) / len(merged_base)
                        merged_lines.append(merged_line)
                        merged_bases.append(merged_mean)
                        merged_indices.add(j)
                        break
            else:
                merged_lines.append(current_line)
                merged_bases.append(sum(current_base) / len(current_base))
    
    return merged_lines

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
    
mean_height = 0
for char in text:
    mean_height += char[1][1] - char[0][1]
mean_height /= len(text)

# lines = getLines(text, mean_height)
# for line in lines:
#     cv.line(mark, line[0], line[1], (255, 0, 0), 5)
lines_pos = getLines(text, mean_height)
lines = [[] for _ in range(len(lines_pos))]
for char in text:
    center = rectCenter(char)
    index = 0
    for i in range(len(lines_pos)):
        if abs(lines_pos[i][1][1] - center[1]) < abs(lines_pos[index][1][1] - center[1]):
            index = i
    lines[index].append(char)
    
for line in lines:
    rect = None
    for char in line:
        if rect is None:
            rect = char
            continue
        rect = (
            (min(char[0][0], rect[0][0]), min(char[0][1], rect[0][1])),
            (max(char[1][0], rect[1][0]), max(char[1][1], rect[1][1]))
        )
    cv.rectangle(mark, rect[0], rect[1], (255, 0, 0), 2)
    
# scale = 150 / len(text)
# for char in range(len(text) - 1):
#     start = rectCenter(text[char])
#     end = rectCenter(text[char + 1])
    
#     cv.line(mark, start, end, (50, 50, 255 - int(scale * char)), 2)

for line in lines:
    for char in range(len(line) - 1):
        start = rectCenter(line[char])
        end = rectCenter(line[char + 1])
        
        cv.line(mark, start, end, (50, 50, 255 - int(scale * char)), 2)
    
cv.imshow('image', mark)
cv.waitKey(0)

# for rect in rects:
#     mark = img.copy()
#     mark = cv.rectangle(mark, rect[0], rect[1], (0, 255, 0), 2)
#     cv.imshow('image', mark)
#     cv.waitKey(0)