from ctypes import *
from win32con import *
import sys
from spaint.colorsec import standlize_color_sec 

WIN8_COLORS_MD = {
 'darkgray': 9,
 'lightblue': 10,
 'brightblue':10,
 'magenta': 6,
 'default': 0,
 'lightmagenta': 14,
 'black': 1,
 'cyan': 4,
 'red': 5,
 'lightcyan': 12,
 'brown': 7,
 'lightgreen': 11,
 'lightred': 13,
 'blue': 2,
 'yellow': 15,
 'lightgray': 8,
 'white': 16,
 'green': 3,
  0: 'default',
 1: 'black',
 2: 'blue',
 3: 'green',
 4: 'cyan',
 5: 'red',
 6: 'magenta',
 7: 'brown',
 8: 'lightgray',
 9: 'darkgray',
 10: 'lightblue',
 11: 'lightgreen',
 12: 'lightcyan',
 13: 'lightred',
 14: 'lightmagenta',
 15: 'yellow',
 16: 'white'
}

WIN8_COLORS_ID2NAME = {
 0: 'default',
 1: 'black',
 2: 'blue',
 3: 'green',
 4: 'cyan',
 5: 'red',
 6: 'magenta',
 7: 'brown',
 8: 'lightgray',
 9: 'darkgray',
 10: 'lightblue',
 11: 'lightgreen',
 12: 'lightcyan',
 13: 'lightred',
 14: 'lightmagenta',
 15: 'yellow',
 16: 'white'
}


WIN8_COLORS_NAME2ID = {
 'darkgray': 9,
 'lightblue': 10,
 'brightblue':10,
 'magenta': 6,
 'default': 0,
 'lightmagenta': 14,
 'black': 1,
 'cyan': 4,
 'red': 5,
 'lightcyan': 12,
 'brown': 7,
 'lightgreen': 11,
 'lightred': 13,
 'blue': 2,
 'yellow': 15,
 'lightgray': 8,
 'white': 16,
 'green': 3
}




STD_OUTPUT_HANDLE = -11

class COORD(Structure):
    _fields_ = [
        ('X', c_short),
        ('Y', c_short),
    ]

class SMALL_RECT(Structure):
    _fields_ = [
        ('Left', c_short),
        ('Top', c_short),
        ('Right', c_short),
        ('Bottom', c_short),
    ]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ('dwSize', COORD),
        ('dwCursorPosition', COORD),
        ('wAttributes', c_uint),
        ('srWindow', SMALL_RECT),
        ('dwMaximumWindowSize', COORD),
    ]


CloseHandle = windll.kernel32.CloseHandle
GetStdHandle = windll.kernel32.GetStdHandle
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute


def print_one(s,fg,bg=1,**kwargs):
    hconsole = GetStdHandle(STD_OUTPUT_HANDLE)
    cmd_info = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(hconsole, byref(cmd_info))
    fg = (fg -1) & 0x0f
    bg = ((bg -1)<<4) & 0xf0
    SetConsoleTextAttribute(hconsole, fg + bg)
    #dont use print("xxxx",end=""),important!
    sys.stdout.write(s)
    sys.stdout.flush()
    if('recover' in kwargs):
        recover = kwargs['recover']
    else:
        recover = True
    if(recover):
        old_color = cmd_info.wAttributes
        SetConsoleTextAttribute(hconsole, old_color)
    else:
        pass
    if('end' in kwargs):
        end = kwargs['end']
    else:
        end = True
    if(end):
        print("")
    else:
        pass


def print_one_with_colorsec(s,color_sec,bg=1,**kwargs):
    hconsole = GetStdHandle(STD_OUTPUT_HANDLE)
    cmd_info = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(hconsole, byref(cmd_info))
    color_sec_len = color_sec.__len__()
    for i in range(1,color_sec_len + 1):
        ele = color_sec[i]
        si = color_sec[i][0]
        ei = color_sec[i][1]
        tmpfg = color_sec[i][2]
        length = ele.__len__()
        if(length == 3):
            tmpbg = bg
        elif(length == 4):
            tmpbg = color_sec[i][3]
        else:
            tmpbg = color_sec[i][3]
        sec = s[si:ei+1]
        tmpfg = (tmpfg -1) & 0x0f
        tmpbg = ((tmpbg -1)<<4) & 0xf0
        SetConsoleTextAttribute(hconsole, tmpfg + tmpbg)
        #dont use print("xxxx",end=""),important!
        sys.stdout.write(sec)
        sys.stdout.flush()
    if('recover' in kwargs):
        recover = kwargs['recover']
    else:
        recover = True
    if(recover):
        old_color = cmd_info.wAttributes
        SetConsoleTextAttribute(hconsole, old_color)
    else:
        pass
    if('end' in kwargs):
        end = kwargs['end']
    else:
        end = True
    if(end):
        print("")
    else:
        pass


def print_str(s,**kwargs):
    if('colors_md' in kwargs):
        colors_md = kwargs['colors_md']
    else:
        colors_md = WIN8_COLORS_MD
    if("fg" in kwargs):
        fg = kwargs['fg']
    else:
        fg = 16
    if("bg" in kwargs):
        bg = kwargs['bg']
    else:
        bg = 1
    if(isinstance(fg,int)):
        pass
    else:
        fg = colors_md[fg]
    if(isinstance(bg,int)):
        pass
    else:
        bg = colors_md[bg]
    if('single_color' in kwargs):
        single_color = kwargs['single_color']
        if(isinstance(single_color,str)):
            single_color = single_color.lower()
            single_color = single_color.replace('bright','light')
            if(single_color in WIN8_COLORS_MD):
                single_color = WIN8_COLORS_MD[single_color]
            else:
                print("please input correct color name")
                pass
        elif(isinstance(single_color,int)):
            pass
        else:
            print("color must be name or int ")
            pass
    else:
        single_color = None
    ####color_sec multicolor for string (si,ei,fg,bg,style), ei is included
    ####"ab" +"bc"
    ####color_sec = {1:(0,1,2),2:(2,3,4)}
    if('color_sec' in kwargs):
        color_sec = kwargs['color_sec']
    else:
        color_sec = None
    if(color_sec):
        del kwargs['color_sec']
        color_sec = standlize_color_sec(color_sec,8,WIN8_COLORS_MD)
        print_one_with_colorsec(s,color_sec,bg,**kwargs)
    else:
        fg = single_color
        print_one(s,fg,bg,**kwargs)


def paint_str(text,**kwargs):
    '''for compatible with old code'''
    return(text)


paint = print_str

def win8_test(fg,**kwargs):
    if(isinstance(fg,int)):
        word = WIN8_COLORS_MD[fg]
    else:
        word = fg.lower()
        fg = WIN8_COLORS_MD[fg]
    print_one(str(fg)+":"+word,fg,1,recover=True,end=True)



def win8_help(*args,**kwargs):
    args = list(args)
    lngth = args.__len__()
    for i in range(0,lngth):
        if(isinstance(args[i],int)):
            pass
        else:
            args[i] = WIN8_COLORS_MD[args[i]]
    if(lngth == 0):
        for name in WIN8_COLORS_NAME2ID:
            i = WIN8_COLORS_NAME2ID[name]
            print_one(str(i) + ": " + name,i,1,recover=True,end=True)
    else:
        for i in range(0,lngth):
            cid = args[i]
            name = WIN8_COLORS_MD[cid]
            print_one(str(cid) + ": " + name,cid,1,recover=True,end=True)

