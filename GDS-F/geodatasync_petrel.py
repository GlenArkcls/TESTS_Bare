# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:20:12 2022

@author: lewthwju
"""


def IDComparison(id0,id1):
    '''Two ids are compared this way because PETREL adds a string into
    IDS for the name of 2D seismic lines, so we test containment not equality for the first field
    Written like this so we don't have to worry about which way round we pass the arguments
    '''
    return (id0[0].count(id1[0])>0 or id1[0].count(id0[0])>0) and id0[1]==id1[1]
    

def startPetrel(port):
    pass