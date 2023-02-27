import math
import re

def get_real_sample_size(text, dis_score):
    if dis_score == None:
        return text
    if text == None or text == '':
        return text
    p = re.compile('\d{1,9}\.{0,1}\d{0,4}')
    t = ''
    arr = []
    text = str(text)
    for a in p.finditer(text):
        arr.append(a)
    i = 0
    ly = None
    for a in arr:
        x = a.span()[0]
        y = a.span()[1]
        if i == 0:
            t += text[0:x]
        if ly != None:
            t += text[ly:x]
        v = float(text[x:y])
        if dis_score == 0:
            v = v * 2
        elif dis_score == 1:
            v = v * 1
        elif dis_score == 2:
            v = v * 1
        elif dis_score == 3:
            v = int(math.ceil(float(v) / 2))
        elif dis_score == 4:
            v = int(math.ceil(float(v) / 2))
        else:
            v = int(math.ceil(float(v) / 4))
        t += str(v)
        if i == len(arr) - 1:
            t += text[y:]
        ly = y
        i += 1
    return t
