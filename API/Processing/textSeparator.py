from .utils import rectCenter, Rects2Rect

def compareTo(rect, reference):
    x, y = rectCenter(rect)
    
    _, y1 = reference[0]
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

def wordCorrector(word):
    temp = []
    for char in word:
        rect = char
        for c in word:
            if char[1][1] < c [0][1] and ((char[0][0] > c[0][0] and char[0][0] < c[1][0]) or (char[1][0] > c[0][0] and char[1][0] < c[1][0])):
                rect = Rects2Rect([rect, c])
        temp.append(rect)
    word.clear()
    word.extend(temp)
    
def orderChars(rects):
    text = []
    for rect in rects:
        if len(text) == 0:
            text.append(rect)
            continue
        orderInsert(text, rect)
    return text

def separeLines(text, mean_height):
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
    
    return lines

def separeWords(line, mean_distance):
    new_line = []
    for char in line:
        if len(new_line) < 1 or max(0, char[0][0] - new_line[-1][-1][1][0]) > mean_distance * 1.5:
            new_line.append([])
        new_line[-1].append(char)
    line = new_line
    
    new_line = []
    for j in range(len(line)):
        word = Rects2Rect(line[j])
        
        if j < 1 or max(0, word[0][0] - Rects2Rect(line[j - 1])[1][0]) > mean_distance:
            new_line.append([])
            
        new_line[-1].extend(line[j])
        
    return new_line