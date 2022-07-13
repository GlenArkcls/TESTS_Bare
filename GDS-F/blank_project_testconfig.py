# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:36:27 2022

@author: lewthwju
"""
import math
import test_config
from seismicgeometry import SeismicGeometry

'''
Ideally we should have unequal spacing
'''
TestSurfGeometry={
        b'SizeI': 7,
        b'SizeJ': 9,
        b'SpacingI': 23.0,
        b'SpacingJ': 13.0,
        b'OriginX': 608271.0,
        b'OriginY': 6076131.0,
        b'Theta': 0.0,
        b'isDepth': 0
        }


'''
Hopefully a sufficiently irregular geometry - actually its theta is 88 degress, probably make it more
rotated
'''


DefaultSeisGeometry={
        b'MinInline': 200,
        b'MaxInline': 218,
        b'InlineInc': 2,
        b'MinXline': 400,
        b'MaxXline': 433,
        b'XlineInc': 3,
        b'X0': 608271.29,
        b'Y0': 6076131.66,
        b'X1': 608406.363659533,
        b'Y1': 6076218.128075472,
        b'X2': 608264.37,
        b'Y2': 6076377.14,
        b'MinZ': 2.014,
        b'MaxZ': 3.858,
        b'ZInc': 0.004,
        b'InlineSep': 23.687,
        b'XlineSep': 22.325228807,
        b'isDepth': 0
        }

'''
Hopefully a sufficiently irregular geometry - actually its theta is 88 degress, probably make it more
rotated
'''
DefaultDepthSeisGeometry={
        b'MinInline': 200,
        b'MaxInline': 218,
        b'InlineInc': 2,
        b'MinXline': 400,
        b'MaxXline': 433,
        b'XlineInc': 3,
        b'X0': 608271.29,
        b'Y0': 6076131.66,
        b'X1': 608406.363659533,
        b'Y1': 6076218.128075472,
        b'X2': 608264.37,
        b'Y2': 6076377.14,
        b'MinZ': 1003.,
        b'MaxZ': 2003.,
        b'ZInc': 5.,
        b'InlineSep': 23.687,
         b'XlineSep': 22.325228807,
        b'isDepth': 1
        }


Default2DSeisGeometry={
        b'isDepth': 0,
        b'XCoords': [608271.6098111111, 608293.5566444445, 608392.8711555556, 608465.1331],
        b'YCoords': [6076155.937466667, 6076229.479022223, 6076256.610711112, 6076355.856044445], 
        b'TraceLength':462,
        b'MinZ':0.014,
        b'ZInc':0.004,
        }

DefaultDepth2DSeisGeometry={
        b'isDepth': 1,
        b'XCoords': [608271.6098111111, 608293.5566444445, 608392.8711555556, 608465.1331],
        b'YCoords': [6076155.937466667, 6076229.479022223, 6076256.610711112, 6076355.856044445], 
        b'TraceLength':462,
        b'MinZ':1003.,
        b'ZInc':5.,
        }

class BlankProjectTestConfig(test_config.TestConfig):
    def __init__(self):
        pass
        
   
    def initialise(self,server,repo):
        pass

    def get3DSeismicGeometry(self,isDepth=False):
        if isDepth:
            return SeismicGeometry(DefaultDepthSeisGeometry)
        else:
            return SeismicGeometry(DefaultSeisGeometry)
    
    
        
    def get3DSeismicData(self,name=None):
         geom=self.get3DSeismicGeometry(False)
         samps=round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1
         baseTraceData=[1.0 + x for x in range(0,samps)]
         ilines,xlines=geom.get3DGeometryILXLPairs()
         volumeData=[[x+y*5 for y in range(len(ilines))] for x in baseTraceData]
         return volumeData
    
    def get2DSeismicGeometry(self,isDepth):
        if isDepth:
            return DefaultDepth2DSeisGeometry 
        else:
            return Default2DSeisGeometry
    
    def get2DLineData(self,name=None):
         baseTraceData=[1.0 + x for x in range(0,self.get2DSeismicGeometry(False)[b'TraceLength'])]
         lineData=[[x+y*5 for y in range(len(self.get2DSeismicGeometry(False)[b'XCoords']))] for x in baseTraceData]
         return lineData
        
   
    def getSurfGeometry(self,isDepth=False):
       if isDepth:
           ret=TestSurfGeometry
           ret[b'isDepth']=1
           return ret
       else:
           return TestSurfGeometry
    
    def getSurfVals(self,name=None):
        return [x +0.1 for x in range(0,self.getSurfGeometry()[b'SizeI']*self.getSurfGeometry()[b'SizeJ'])]
    
    def getHorizonVals(self,name=None):
       geom=self.get3DSeismicGeometry(False)
       inlines=(geom.getMaxInline()-geom.getMinInline())/geom.getInlineInc()+1
       xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
       minz=geom.getMinZ()
       maxz=geom.getMaxZ()
       z0=(minz+maxz)/2
       return [z0 +0.001*float(il-geom.getMinInline()) -0.001*float(xl-geom.getMinXline()) for il in range(0,int(inlines)) for xl in range(0,int(xlines))]
    
    def getHorizonPropertyVals(self,name=None):
        geom=self.get3DSeismicGeometry(False)
        inlines=(geom.getMaxInline()-geom.getMinInline())/geom.getInlineInc()+1
        xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
        return [1.0 -0.1*float(il-geom.getMinInline()) +0.1*float(xl-geom.getMinXline()) for il in range(0,int(inlines)) for xl in range(0,int(xlines))]
   
    def getWellHeadCoordinates(self,name=None):
        geom=self.get3DSeismicGeometry(False)
        return [(geom.getX1()+geom.getX0())/2,(geom.getY1()+geom.getY0())/2]
    
    def getWellTrack(self,name=None):
        geom=self.get3DSeismicGeometry(False)
        xcoords=[((geom.getX1()+geom.getX0())/2+math.exp(x/30.)) for x in range(0,100)]
        ycoords=[((geom.getY1()+geom.getY0())/2+math.exp(-y/20.)) for y in range(0,100)]
        z=[10.*z for z in range(0,100)]
        reftype=b"KB"
        reflevel=-25.
        return {"X":xcoords,"Y":ycoords,"Z":z,"reftype":reftype,"reflevel":reflevel}
    
    def getWellLogData(self,param=0):
        if param==0:
            logVals=[math.sin(x)*10 for x in range(0,100)]
        else:
            logVals=[math.cos(x)*10 for x in range(0,100)]
        return {"Values":logVals,"Start":10.,"Interval":10.}
    
    
    def getFaultData(self,name=None):
        xcoords=[608300.2,608301.3,608302.5,608320.1,608324.3,608330.2,608330.4,608340.3,608346.2,608348.2]
        ycoords=[6076200.1,6076203.2,6076208.3,6076230.5,6076236.3,6076240.4,6076240.6,6076290.4,6076298.3,6076302.2]
        zcoords=[1.0,1.1,1.2,1.05,1.16,1.21,1.23,1.11,1.20,1.26]
        fdata={"sticks":3,"points":[3,4,3],"xcoords":xcoords,"ycoords":ycoords,"zcoords":zcoords}
        return fdata
    
    def getPointSetData(self,isDepth=False):
        xcoords=[608300.2,608301.3,608302.5,608320.1,608324.3,608330.2,608330.4,608340.3,608346.2,608348.2]
        ycoords=[6076200.1,6076203.2,6076208.3,6076230.5,6076236.3,6076240.4,6076240.6,6076290.4,6076298.3,6076302.2]
        
        if isDepth:
            zcoords=[2000.,2005.,2010.,2002.5,2008.,2010.5,2011.5,2005.5,2010.,2013.]
            return {"XCoords":xcoords,"YCoords":ycoords,"ZCoords":zcoords,"isDepth":1}
        
        else:
            zcoords=[1.0,1.1,1.2,1.05,1.16,1.21,1.23,1.11,1.20,1.26]
            return {"XCoords":xcoords,"YCoords":ycoords,"ZCoords":zcoords,"isDepth":0}
    
    def getWaveletData(self,name=None):
        v=[(10*math.cos(x-50))/((x-50)*(x-50)+1) for x in range(0,101)]
        return {"SampleInt":0.01,"Wavelet":v}
    
    def getPolygonData(self,isDepth=False):
        polylines=3
        pointsInLine=[3,4,3]
        xcoords=[608300.2,608301.3,608302.5,608320.1,608324.3,608330.2,608330.4,608340.3,608346.2,608348.2]
        ycoords=[6076200.1,6076203.2,6076208.3,6076230.5,6076236.3,6076240.4,6076240.6,6076290.4,6076298.3,6076302.2]
        if isDepth:
            zcoords=[2000.,2000.,2000.,2002.5,2002.5,2010.,2010.,2020.,2020.,2020.]
            isDepth=1
        else:
            zcoords=[1.0,1.0,1.0,1.05,1.05,1.2,1.2,1.4,1.4,1.4]
            isDepth=0
        areClosed=[0,1,0]
        return {"Polylines":polylines,"Points":pointsInLine,"XCoords":xcoords,"YCoords":ycoords,"ZCoords":zcoords,"IsDepth":isDepth,"Closed":areClosed}
        
        