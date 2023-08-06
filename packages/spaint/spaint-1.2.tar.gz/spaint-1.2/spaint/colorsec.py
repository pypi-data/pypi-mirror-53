import copy
from spaint.ansi256 import *
from spaint.ansi8 import *
from spaint.common import *


def old_stylize_colorsec(color_sec):
    '''
        for compatible with old code
        old_style_color_sec = {1: (0, 11, 'white'), 2: (12, 19, 'blue'), 3: (20, 21, 'white')}
        new_style_color_sec = [(0, 12, 'white'), (12, 20, 'blue'), (20, 22, 'white')]
        old_stylize_colorsec(new_style_color_sec)
    '''
    if(isinstance(color_sec,dict)):
        return(copy.copy(color_sec))
    else:
        pass
    new = {}
    for i in range(0,color_sec.__len__()):
        sec = color_sec[i]
        new[i+1] = copy.copy(list(sec))
        new[i+1][1] = sec[1] - 1
        new[i+1] = tuple(new[i+1])
    return(new)

def new_stylize_colorsec(color_sec):
    '''
        for compatible with old code
        old_style_color_sec = {1: (0, 11, 'white'), 2: (12, 19, 'blue'), 3: (20, 21, 'white')}
        new_style_color_sec = [(0, 12, 'white'), (12, 20, 'blue'), (20, 22, 'white')]
        new_stylize_colorsec(old_style_color_sec)
    '''
    if(isinstance(color_sec,list)):
        return(copy.copy(color_sec))
    else:
        pass
    new = []
    for i in range(0,color_sec.__len__()):
        sec = color_sec[i+1]
        sec = copy.copy(list(sec))
        sec[1] = sec[1] + 1
        sec = tuple(sec)
        new.append(sec)
    return(new)

def standlize_color_sec(color_sec,mode,colors_md):
    #now we can accept either new_style_color_sec or old_style_color_sec
    #the internal function use old_style_color_sec
    color_sec = old_stylize_colorsec(color_sec)
    new = {}
    for seq in color_sec:
        sec = color_sec[seq]
        color = sec[2]
        if(isinstance(color,str)):
            color = color.lower()
            if(mode == 256):
                color = name2colorId(color)
            else:
                if(is_win()):
                    color = color.replace('bright','light')
                else:
                    color = color.replace('light','bright')
                color = colors_md[color]
        else:
            pass
        new[seq] = copy.copy(list(sec))
        new[seq][2] = color
        ######## bgcolor
        try:
            bgcolor = sec[3]
        except:
            pass
        else:
            if(isinstance(bgcolor,str)):
                bgcolor = bgcolor.lower()
                if(mode == 256):
                    bgcolor = name2colorId(bgcolor)
                else:
                    if(is_win()):
                        bgcolor = bgcolor.replace('bright','light')
                    else:
                        bgcolor = bgcolor.replace('light','bright')
                    bgcolor = colors_md[bgcolor]
            else:
                pass
            new[seq][3] = bgcolor
        ##########
        new[seq] = tuple(new[seq])
    return(new)

