# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 08:42:09 2022

@author: lewthwju
"""

#from overloading import overload
from collections.abc import Iterable
import types
from constants import *
import numpy as np
import matplotlib

class MyC:
    def __init__(self,index):
        self.__index=index
        self._index=index
        

myC=MyC(5)

print(myC._index)
print(myC.__index)

def myfunc2(*args):
    ret=1
    
    for arg in args:
        ret=ret*arg
    return ret

def myfunc(*args):
    ret=1
    l=[]
    for arg in args:
        l.append(arg)
    print(l)
    return myfunc2(*l)
        
def mess():
    global CONST0
    CONST0="bye again"

a=myfunc(2,3)
print(a)

#t=(2,3,4)
t=[2,3,4]

b=myfunc(*t)
print(b)

SEISMIC0="Seismic0"

STRA="Here is '{}'".format(SEISMIC0)
print(STRA)



#def docstrtest()->"boo":
#    '''Testing output the docstring.
#    
#    So now we should have a detailed
#    explanation here.
#    '''
#    
#    pass
##def flatten(ob):
##    yield ob
##    
##@overload
##def flatten(ob:Iterable):
##    for o in ob:
##        for ob in flatten(o):
##            yield ob
##
##@overload
##def flatten(ob:basestring):
##    yield ob
#    
#    
#
#print(docstrtest.__doc__)
#print(docstrtest.__annotations__)