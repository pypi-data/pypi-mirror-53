from spaint.ansi256 import *
from spaint.ansi8 import *
from spaint.colorsec import *

#for compatible with old code
def print_str(text,**kwargs):
    print(text)

def paint_str(orig_string,**kwargs):
    '''
        currently only support 8 color name,
        if using 256 color need using color number
    '''
    default =  "\033[0m"
    painted_string = default
    #####mode
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 256
    if(mode == 8):
        color_control = ansi_8color_control
        COLORS_MD = ANSI8_COLORS_MD
    elif(mode == 256):
        color_control = ansi_256color_control
        COLORS_MD = ANSI256_COLORS_MD
    else:
        print("mode : " +mode +"not supported!,fallback to 8color ")
        color_control = ansi_256color_control
    ######color name<->number mapping
    if('colors' in kwargs):
        colors_md = kwargs['colors']
    else:
        colors_md = COLORS_MD
    ####singlecolor for string
    if("bg" in kwargs):
        bg = kwargs['bg']
    else:
        bg = 30
    if("style" in kwargs):
        style = kwargs['style']
    else:
        style = 1
    if('single_color' in kwargs):
        single_color = kwargs['single_color']
        if(isinstance(single_color,str)):
            single_color = single_color.lower()
            single_color = single_color.replace('light','bright')
            if(single_color in COLORS_MD):
                single_color = COLORS_MD[single_color]
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
    ####color_sec = {1:(0,1,'blue'),2:(2,3,'green')}
    if('color_sec' in kwargs):
        color_sec = kwargs['color_sec']
    else:
        color_sec = None
    if(color_sec):
        color_sec = standlize_color_sec(color_sec,mode,COLORS_MD)
        color_sec_len = color_sec.__len__()
        for i in range(1,color_sec_len + 1):
            ele = color_sec[i]
            si = color_sec[i][0]
            ei = color_sec[i][1]
            fg = color_sec[i][2]
            length = ele.__len__()
            if(length == 3):
                color = color_control(fg=fg)
            elif(length == 4):
                bg = color_sec[i][3]
                color = color_control(fg=fg,bg=bg)
            else:
                bg = color_sec[i][3]
                style = color_sec[i][4]
                color = color_control(fg=fg,bg=bg,style=style)
            sec = ''.join((color,orig_string[si:ei+1]))
            painted_string = ''.join((painted_string,sec))
        painted_string = ''.join((painted_string,default))
    else:
        fg = single_color
        bg = bg
        style = style
        color = color_control(fg=fg,bg=bg,style=style)
        painted_string = ''.join((painted_string,color,orig_string,default))
    return(painted_string)


def paint(s,**kwargs):
    if('lend' in kwargs):
        lend = kwargs['lend']
    else:
        lend = '\n'
    if('rtrn' in kwargs):
        rtrn = kwargs['rtrn']
    else:
        rtrn = False
    if(rtrn):
        return(paint_str(s,**kwargs))
    else:
        print(paint_str(s,**kwargs),end=lend)

