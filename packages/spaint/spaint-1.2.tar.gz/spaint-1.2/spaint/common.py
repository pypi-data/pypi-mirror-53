import os
import sys

##str
def str_rstrip(s,char,count):
    '''
        str_rstrip('asss','s',0)
        str_rstrip('asss','s',1)
        str_rstrip('asss','s',2)
        str_rstrip('asss','s',3)
        str_rstrip('asss','s',4)
    '''
    c = 0
    for i in range(s.__len__()-1,-1,-1):
        if(c==count):
            break
        else:
            if(s[i] == char):
                c = c+1
            else:
                break
    if(c==0):
        return(s)
    else:
        ei = s.__len__() - c
        return(s[:ei])


##platform
def is_win():
    platform = os.sys.platform.lower()
    if('win' in platform):
        return(True)
    else:
        return(False)
##########

