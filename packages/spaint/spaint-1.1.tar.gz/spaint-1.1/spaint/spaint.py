import copy
import elist.elist as elel
import random
from spaint.common import *

#####engine######
if(is_win()):
    from spaint.win8 import *
else:
    from spaint.ansi256 import *
    from spaint.ansi8 import *
    from spaint.linux import *
    

#################################################
def fullfill_colors(spans,old_spans,colors,default_color):
    rslt = []
    lngth = spans.__len__()
    for i in range(0,lngth):
        cond = (spans[i] in old_spans)
        if(cond):
            index = old_spans.index(spans[i])
            color = colors[index]
        else:
            color = default_color
        rslt.append(color)
    return(rslt)
################################################

def fmt_span(span,lngth):
    x = elel.uniform_index(span[0],lngth)
    y = elel.uniform_index(span[1],lngth)
    l = sorted([x,y])
    return(tuple(l))


###############################################
def spanpaint(s,*args,**kwargs):
    def map_func(span,color):
        return((span[0],span[1],color))
    if('default_color' in kwargs):
        default_color = kwargs['default_color']
    else:
        default_color = 'white'
    args = list(args)
    old_spans = elel.select_evens(args)
    lngth = s.__len__()
    old_spans = elel.mapv(old_spans,fmt_span,[lngth])
    colors = elel.select_odds(args)
    spans = elel.rangize_fullfill(old_spans,lngth)
    ###debug
    ###debug
    colors = fullfill_colors(spans,old_spans,colors,default_color)
    color_sec = elel.array_map2(spans,colors,map_func=map_func)
    #debug
    #debug
    return(paint(s,color_sec=color_sec,**kwargs))


def sieipaint(s,*args,**kwargs):
    def map_func(span,color):
        return((span[0],span[1],color))
    if('default_color' in kwargs):
        default_color = kwargs['default_color']
    else:
        default_color = 'white'
    args = list(args)
    tmp = elel.deinterleave(args,3)
    sis = tmp[0]
    eis = tmp[1]
    colors = tmp[2]
    old_spans = elel.mapiv(sis,lambda index,ele:((ele,eis[index])),[])
    lngth = s.__len__()
    spans = elel.rangize_fullfill(old_spans,lngth)
    colors = fullfill_colors(spans,old_spans,colors,default_color)
    color_sec = elel.array_map2(spans,colors,map_func=map_func)
    return(paint(s,color_sec=color_sec,**kwargs))


def get_eis_from_sis(sis,lngth):
    sis.sort()
    eis = []
    for i in range(1,sis.__len__()):
        ei = sis[i]
        if(ei<lngth):
            eis.append(ei)
        else:
            eis.append(lngth)
            break
    eis.append(lngth)
    return(eis)

def sipaint(s,*args,**kwargs):
    def map_func(span,color):
        return((span[0],span[1],color))
    if('default_color' in kwargs):
        default_color = kwargs['default_color']
    else:
        default_color = 'white'
    args = list(args)
    tmp = elel.deinterleave(args,2)
    sis = tmp[0]
    colors = tmp[1]
    eis = get_eis_from_sis(sis,s.__len__())
    old_spans = elel.mapiv(sis,lambda index,ele:((ele,eis[index])),[])
    lngth = s.__len__()
    spans = elel.rangize_fullfill(old_spans,lngth)
    colors = fullfill_colors(spans,old_spans,colors,default_color)
    color_sec = elel.array_map2(spans,colors,map_func=map_func)
    return(paint(s,color_sec=color_sec,**kwargs))


def get_sis_from_eis(eis,lngth):
    eis.sort()
    if(eis[-1]>lngth):
        eis[-1] = lngth
    else:
        pass
    sis = [0]
    for i in range(0,eis.__len__()-1):
        si = eis[i] 
        sis.append(si)
    return(sis)



def eipaint(s,*args,**kwargs):
    def map_func(span,color):
        return((span[0],span[1],color))
    if('default_color' in kwargs):
        default_color = kwargs['default_color']
    else:
        default_color = 'white'
    args = list(args)
    tmp = elel.deinterleave(args,2)
    eis = tmp[0]
    colors = tmp[1]
    sis = get_sis_from_eis(eis,s.__len__())
    old_spans = elel.mapiv(sis,lambda index,ele:((ele,eis[index])),[])
    lngth = s.__len__()
    spans = elel.rangize_fullfill(old_spans,lngth)
    colors = fullfill_colors(spans,old_spans,colors,default_color)
    color_sec = elel.array_map2(spans,colors,map_func=map_func)
    return(paint(s,color_sec=color_sec,*kwargs))




####



def slpaint(*args,**kwargs):
    '''
        slpaint('<div>','yellow','content','green','</div>','yellow')
    '''
    args = list(args)
    strs = elel.select_evens(args)
    colors = elel.select_odds(args)
    lngth = strs.__len__()
    spans = []
    si = 0
    ei = 0
    for i in range(0,lngth):
        ei = si + strs[i].__len__()
        color = colors[i]
        span = (si,ei,color)
        spans.append(span)
        si = ei
    s = elel.join(strs,'')
    return(paint(s,color_sec=spans,**kwargs))


    

def mlpaint(lines,colors,**kwargs):
    '''
        lines = [
            'the first green line',
            'the second yellow line',
            'the third blue line'
        ]
        
        colors = ['green','yellow','blue']
        mlpaint(lines,colors)
    '''
    if('line_sp' in kwargs):
        line_sp = kwargs['line_sp']
    else:
        line_sp = '\n'
    s = ''
    length = lines.__len__()
    clen = colors.__len__()
    if(clen < length):
        colors = copy.copy(colors)
        colors.extend(['white'] * (length-clen))
    else:
        pass
    color_sec = {}
    cursor = 0
    for i in range(0,length):
        line = lines[i] + line_sp
        llen = line.__len__()
        color = colors[i]
        color_sec[i+1] = (cursor,cursor+llen-1,color)
        cursor = cursor + llen
        s = s + line
    s = str_rstrip(s,line_sp,1)
    return(paint(s,color_sec=color_sec,**kwargs))


#####

def rainbow(s,interval=1,**kwargs):
    if('rand' in kwargs):
        rand = kwargs['rand']
    else:
        rand = True
    if('color_plan' in kwargs):
        color_plan = kwargs['color_plan']
    else:
        color_plan = ['red','white','yellow','green','blue']
    lngth = s.__len__()
    bpts = elel.init_range(0,lngth,interval)
    spans = elel.rangize(bpts,lngth)
    args = []
    if(rand):
        arr = elel.init(lngth)
        if(is_win()):
            color_plan = elel.mapv(arr,lambda ele:WIN8_COLORS_MD[random.randint(0,15)],[])
        else:
            color_plan = elel.mapv(arr,lambda ele:ANSI256_COLORS_ID2NAME[random.randint(0,255)],[])
    else:
        color_plan = color_plan * (lngth // color_plan.__len__() + 1)
        color_plan = color_plan[:lngth]
    args = elel.interleave(spans,color_plan)
    return(spanpaint(s,*args,**kwargs))


def rainbow_lines(lines,interval=1,**kwargs):
    if('rand' in kwargs):
        rand = kwargs['rand']
    else:
        rand = True
    if('color_plan' in kwargs):
        color_plan = kwargs['color_plan']
    else:
        color_plan = ['red','white','yellow','green','blue']
    if('line_sp' in kwargs):
        line_sp = kwargs['line_sp']
    else:
        line_sp = '\n'
    lngth = lines.__len__()
    if(rand):
        arr = elel.init(lngth)
        if(is_win()):
            color_plan = elel.mapv(arr,lambda ele:WIN8_COLORS_MD[random.randint(0,15)],[])
        else:
            color_plan = elel.mapv(arr,lambda ele:ANSI256_COLORS_ID2NAME[random.randint(0,255)],[])
    else:
        color_plan = color_plan * (lngth // color_plan.__len__() + 1)
        color_plan = color_plan[:lngth]
    color_plan = elel.repeat_every(color_plan,interval)
    return(mlpaint(lines,color_plan,**kwargs))

