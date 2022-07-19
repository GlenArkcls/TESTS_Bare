# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:02:13 2022

@author: lewthwju

This file will just contain various utility methods
"""

import math

GeoDataSync=None

FLOAT_COMP_TOL=0.0001

def IDInList(IDComp,theID,theList):
    '''Searches for a given ID in a list using
    the given IDComp function as an equality check
    '''
    if theList==None or theID==None:
        return False
    matches=[x for x in theList if IDComp(theID,x)]
    return len(matches)>0

def getNearestIntegerInRange(rng,testVal):
    if testVal<rng.start:
        return rng.start
    normTest=(testVal-rng.start)/rng.step
    ret= round(normTest)*rng.step+rng.start
    while ret>rng.stop:
        ret-=rng.step
    return ret

def compareNestedFloatLists(l0,l1):
    '''
    Compare two float list of lists that element wise are within the tolerance
    ''' 
    if l0 is None or l1 is None:
        return l0 is None and l1 is None
    
    if len(l0)!=len(l1):
        return False
    for i in range(0,len(l0)):
        if not compareFloatLists(l0[i],l1[i]):
            return False
    return True

def bilinearValueInterp(cornerVals,dist0,dist1):
    a=(cornerVals[0]*(1-dist0)*(1-dist1))
    b=(cornerVals[1]*(1-dist0)*(dist1))
    c=(cornerVals[2]*(dist0)*(1-dist1))
    d=(cornerVals[3]*(dist0)*(dist1))
    ret=a
    if not math.isnan(b):
        ret=ret+b
    if not math.isnan(c):
        ret=ret+c
    if not math.isnan(d):
        ret=ret+d
    return ret
    
def bilinearTraceInterp(dist0,dist1,cornerTraces):
    '''
    dist0,dist1 are the two normalised (ie in range 0,1) distances fromj the corners
    cornerTraces are the four traces (just data) at these corner points
    '''
    ret=[]
    for i in range(0,len(cornerTraces)):
        vals=[cornerTraces[i][0],cornerTraces[i][1],cornerTraces[i][2],cornerTraces[i][3]]
        ret.append(bilinearValueInterp(vals,dist0,dist1))
    return ret

def compareFloatLists(l0,l1):
    '''
    Compare two float lists that element wise are within the tolerance
    ''' 
    if l0 is None or l1 is None:
        return l0 is None and l1 is None
    
    if len(l0)!=len(l1):
        return False
    for i in range(0,len(l0)):
        if math.isnan(l0[i]) or math.isnan(l1[i]):
            if not (math.isnan(l0[i]) and math.isnan(l1[i])):
                return False
        elif abs(l0[i]-l1[i])>FLOAT_COMP_TOL:
            #print("Failed at {} {} {}".format(i,l0[i],l1[i]))
            return False
    return True


def GDSErr(server,baseMsg):
    '''
    Safe way to get the last error message - just in case it throws an exception
    '''
    try:
        errMsg=GeoDataSync("getLastError",server)
        return baseMsg+" "+str(errMsg,"utf-8")
    except:
        return baseMsg+"(No GDS err)"

def compareGeometries(geom1,geom2):
    '''
    Makes sure the floats are compared within a tolerance and the volID field is excluded
    from the comparison
    '''
    return (geom1[b'MinInline']==geom2[b'MinInline'] and
        geom1[b'MaxInline']==geom2[b'MaxInline'] and
        geom1[ b'InlineInc']==geom2[b'InlineInc'] and
        geom1[ b'MinXline']==geom2[b'MinXline'] and
        geom1[ b'MaxXline']==geom2[b'MaxXline'] and
        geom1[ b'XlineInc']==geom2[b'XlineInc'] and
        geom1[ b'MinZ']==geom2[b'MinZ'] and
        geom1[b'MaxZ']==geom2[b'MaxZ'] and
        geom1[ b'ZInc']==geom2[b'ZInc'] and
        abs(geom1[b'X0']-geom2[b'X0'])<FLOAT_COMP_TOL and
        abs(geom1[b'Y0']-geom2[b'Y0']) <FLOAT_COMP_TOL and
        abs(geom1[ b'X1']-geom2[ b'X1']) <FLOAT_COMP_TOL and
        abs(geom1[ b'Y1']- geom2[b'Y1']) <FLOAT_COMP_TOL and
        abs(geom1[ b'X2']-geom2[b'X2']) <FLOAT_COMP_TOL and
        abs(geom1[ b'Y2']- geom2[b'Y2']) <FLOAT_COMP_TOL and
        geom1[ b'isDepth']==geom2[b'isDepth']  and
        abs(geom1[b'InlineSep']-geom2[b'InlineSep']) <FLOAT_COMP_TOL and
        abs(geom1[b'XlineSep']-geom2[b'XlineSep'])<FLOAT_COMP_TOL)

'''
The fields to create a geometry are slightly different from that returned from
a 'getSeisGeometry' call, 
two are missing and the order is different
'''       
def makeCreationGeometryFromFullGeometry(geometry):
    return {
        b'MinInline': geometry[b'MinInline'],
        b'MaxInline': geometry[b'MaxInline'],
        b'InlineInc': geometry[b'InlineInc'],
        b'MinXline': geometry[b'MinXline'],
        b'MaxXline': geometry[b'MaxXline'],
        b'XlineInc': geometry[b'XlineInc'],
        b'MinZ': float(geometry[b'MinZ']),
        b'MaxZ': float(geometry[b'MaxZ']),
        b'ZInc': float(geometry[b'ZInc']),
        b'X0': geometry[b'X0'],
        b'Y0': geometry[b'Y0'],
        b'X1':geometry[ b'X1'],
        b'Y1': geometry[b'Y1'],
        b'X2': geometry[b'X2'],
        b'Y2': geometry[b'Y2'],
        b'isDepth':geometry[b'isDepth']
        } 
    

def compareSurfGeometries(geom1,geom2):
       return (geom1[b'SizeI']==geom2[b'SizeI'] and
               geom1[b'SizeJ']==geom2[b'SizeJ'] and
               geom1[b'SpacingI']-geom2[b'SpacingI'] <FLOAT_COMP_TOL and
               geom1[b'SpacingJ']-geom2[b'SpacingJ'] <FLOAT_COMP_TOL and
               geom1[b'OriginX']-geom2[b'OriginX'] <FLOAT_COMP_TOL and
               geom1[b'OriginY']-geom2[b'OriginY'] <FLOAT_COMP_TOL and
               geom1[b'Theta']-geom2[b'Theta'] <FLOAT_COMP_TOL and
               geom1[b'isDepth']==geom2[b'isDepth'])
   
        


def initModule(geodatasyncFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn
    
# if __name__=="__main__":
#     print(getNearestIntegerInRange(range(5,28,4),6.7))
#     print(getNearestIntegerInRange(range(5,28,4),23.1))
#     print(getNearestIntegerInRange(range(5,28,4),27))
#     for x in range(5,28,4):
#         print(x)
        

    