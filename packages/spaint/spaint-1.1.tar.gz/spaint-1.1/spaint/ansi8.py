ANSI8_COLORS_MD = {
    'black': 30,
    'red': 31,
    'brightwhite': 97,
    'brightyellow': 93,
    97: 'brightwhite',
    'brightblack': 90,
    'brightred': 91,
    'blue': 34,
    'brightcyan': 96,
    'lightcyan': 96,
    'brightmagenta': 95,
    90: 'brightblack',
    91: 'brightred',
    'white': 37,
    93: 'brightyellow',
    30: 'black',
    31: 'red',
    32: 'green',
    33: 'yellow',
    34: 'blue',
    35: 'magenta',
    36: 'cyan',
    37: 'white',
    'cyan': 36,
    92: 'brightgreen',
    95: 'brightmagenta',
    'brightgreen': 92,
    'lightgreen': 92,
    'magenta': 35,
    96: 'brightcyan',
    'green': 32,
    94: 'brightblue',
    'brightblue': 94,
    'lightblue':94,
    'yellow': 33
}


ANSI8_COLORS_ID2NAME = {
    97: 'brightwhite',
    90: 'brightblack',
    91: 'brightred',
    93: 'brightyellow',
    30: 'black',
    31: 'red',
    32: 'green',
    33: 'yellow',
    34: 'blue',
    35: 'magenta',
    36: 'cyan',
    37: 'white',
    92: 'brightgreen',
    95: 'brightmagenta',
    96: 'brightcyan',
    94: 'brightblue',
}


ANSI8_COLORS_NAME2ID = {
    'black': 30,
    'red': 31,
    'brightwhite': 97,
    'brightyellow': 93,
    'brightblack': 90,
    'brightred': 91,
    'blue': 34,
    'brightcyan': 96,
    'lightcyan': 96,
    'brightmagenta': 95,
    'white': 37,
    'cyan': 36,
    'brightgreen': 92,
    'lightgreen': 92,
    'magenta': 35,
    'green': 32,
    'brightblue': 94,
    'lightblue':94,
    'yellow': 33
}



def ansi_8color_control(**kwargs):
    '''
        The original specification only had 8 colors, and just gave them names.
        The SGR parameters 30-37 selected the foreground color,
        while 40-47 selected the background.
        Quite a few terminals implemented "bold" (SGR code 1)
        as a brighter color rather than a different font,
        thus providing 8 additional foreground colors.
        Usually you could not get these as background colors,
        though sometimes inverse video (SGR code 7) would allow that.
        Examples: to get black letters on white background use ESC[30;47m, to get red use ESC[31m,
        to get bright red use ESC[1;31m. To reset colors to their defaults,
        use ESC[39;49m (not supported on some terminals), or reset all attributes with ESC[0m.
        Later terminals added the ability to directly specify the "bright" colors with 90-97 and 100-107.
    '''
    if("fg" in kwargs):
        fg = kwargs['fg']
    else:
        fg = 37
    if("bg" in kwargs):
        bg = kwargs['bg']
    else:
        bg = 30
    bg = bg + 10
    if("style" in kwargs):
        style = kwargs['style']
    else:
        style = 1
    control = '\033[' + str(style)+ ";" +str(fg) +";"+str(bg) +"m"
    return(control)



def ansi8_test(fg,**kwargs):
    if(isinstance(fg,int)):
        word = ANSI8_COLORS_MD[fg]
    else:
        word = fg.lower()
        fg = ANSI8_COLORS_MD[fg]
    default =  "\033[0m"
    s = ansi_8color_control(fg=fg,bg=0)+str(fg) + ":" + word+default
    if('rtrn' in kwargs):
        return(s)
    else:
        print(s)


def ansi8_help(*args,**kwargs):
    args = list(args)
    lngth = args.__len__()
    for i in range(0,lngth):
        if(isinstance(args[i],int)):
            pass
        else:
            args[i] = ANSI8_COLORS_MD[args[i]]
    if(lngth == 0):
        for name in ANSI8_COLORS_NAME2ID:
            i = ANSI8_COLORS_NAME2ID[name]
            print(str(i) + ": " + ansi8_test(name,rtrn=True))
    else:
        for i in range(0,lngth):
            print(str(args[i])+": " + ansi8_test(args[i],rtrn=True))

