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
Hopefully a sufficiently irregular geomerty - actually its theta is 88 degress, probably make it more
rotated
'''
DefaultSeisGeometry={
        b'MinInline': 200,
        b'MaxInline': 218,
        b'InlineInc': 2,
        b'MinXline': 400,
        b'MaxXline': 427,
        b'XlineInc': 3,
        b'X0': 608271.29,
        b'Y0': 6076131.66,
        b'X1': 608406.363659533,
        b'Y1': 6076218.128075472,
        b'X2': 608264.37,
        b'Y2': 6076377.14,
        b'MinZ': 0.014,
        b'MaxZ': 1.858,
        b'ZInc': 0.004,
        b'InlineSep': 23.687,
        b'XlineSep': 27.2863908,
        b'isDepth': 0
        }


Default2DSeisGeometry={
        b'isDepth': 0,
        b'XCoords': [608271.6098111111, 608293.5566444445, 608392.8711555556, 608465.1331],
        b'YCoords': [6076155.937466667, 6076229.479022223, 6076256.610711112, 6076355.856044445], 
        b'TraceLength':462,
        b'MinZ':0.014,
        b'ZInc':0.004,
        }

class BlankProjectTestConfig(test_config.TestConfig):
    def __init__(self):
        pass
        
   
    def initialise(self,server,repo):
        pass

    def get3DSeismicGeometry(self,name=None):
        return SeismicGeometry(DefaultSeisGeometry)
    
    
        
    def get3DSeismicData(self,name=None):
         geom=self.get3DSeismicGeometry()
         samps=round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1
         baseTraceData=[1.0 + x for x in range(0,samps)]
         ilines,xlines=geom.get3DGeometryILXLPairs()
         volumeData=[[x+y*5 for y in range(len(ilines))] for x in baseTraceData]
         return volumeData
    
    def get2DSeismicGeometry(self,name=None):
        return Default2DSeisGeometry 
    
    def get2DLineData(self,name=None):
         baseTraceData=[1.0 + x for x in range(0,self.get2DSeismicGeometry()[b'TraceLength'])]
         lineData=[[x+y*5 for y in range(len(self.get2DSeismicGeometry()[b'XCoords']))] for x in baseTraceData]
         return lineData
        
   
    def getSurfGeometry(self,name=None):
       return TestSurfGeometry
    
    def getSurfVals(self,name=None):
        return [x +0.1 for x in range(0,self.getSurfGeometry()[b'SizeI']*self.getSurfGeometry()[b'SizeJ'])]
    
    def getHorizonVals(self,name=None):
        geom=self.get3DSeismicGeometry()
        inlines=(geom.getMaxInline()-geom.getMinInline())/geom.getInlineInc()+1
        xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
        return [1.0 +0.1*float(il-geom.getMinInline()) -0.1*float(xl-geom.getMinXline()) for il in range(0,int(inlines)) for xl in range(0,int(xlines))]
    
    def getHorizonPropertyVals(self,name=None):
        geom=self.get3DSeismicGeometry()
        inlines=(geom.getMaxInline()-geom.getMinInline())/geom.getInlineInc()+1
        xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
        return [1.0 -0.1*float(il-geom.getMinInline()) +0.1*float(xl-geom.getMinXline()) for il in range(0,int(inlines)) for xl in range(0,int(xlines))]
   
    def getWellHeadCoordinates(self,name=None):
        geom=self.get3DSeismicGeometry()
        return [(geom.getX1()+geom.getX0())/2,(geom.getY1()+geom.getY0())/2]
    
    def getWellTrack(self,name=None):
        geom=self.get3DSeismicGeometry()
        xcoords=[-((geom.getX1()+geom.getX0())/2+math.exp(x/30.)) for x in range(0,100)]
        ycoords=[-((geom.getY1()+geom.getY0())/2+math.exp(-y/20.)) for y in range(0,100)]
        z=[10.*z for z in range(0,100)]
        reftype=b"KB"
        reflevel=-25.
        return {"X":xcoords,"Y":ycoords,"Z":z,"reftype":reftype,"reflevel":reflevel}
    
    def getWellLogData0(self,name=None):
        logVals=[math.sin(x)*10 for x in range(0,100)]
        return {"Values":logVals,"Start":10.,"Interval":10.}
    def getWellLogData1(self,name=None):
        logVals=[math.cos(x)*10 for x in range(0,100)]
        return {"Values":logVals,"Start":10.,"Interval":10.}
    
    def getFaultData(self,name=None):
        xcoords=[608300.2,608301.3,608302.5,608320.1,608324.3,608330.2,608330.4,608340.3,608346.2,608348.2]
        ycoords=[6076200.1,6076203.2,6076208.3,6076230.5,6076236.3,6076240.4,6076240.6,6076290.4,6076298.3,6076302.2]
        zcoords=[1.0,1.1,1.2,1.05,1.16,1.21,1.23,1.11,1.20,1.26]
        fdata={"sticks":3,"points":[3,4,3],"xcoords":xcoords,"ycoords":ycoords,"zcoords":zcoords}
        return fdata
    
    def getPointSetData(self,name=None):
        xcoords=[608300.2,608301.3,608302.5,608320.1,608324.3,608330.2,608330.4,608340.3,608346.2,608348.2]
        ycoords=[6076200.1,6076203.2,6076208.3,6076230.5,6076236.3,6076240.4,6076240.6,6076290.4,6076298.3,6076302.2]
        zcoords=[1.0,1.1,1.2,1.05,1.16,1.21,1.23,1.11,1.20,1.26]
        return {"XCoords":xcoords,"YCoords":ycoords,"ZCoords":zcoords}
    
    def getWaveletData(self,name=None):
        v=[(10*math.cos(x-50))/((x-50)*(x-50)+1) for x in range(0,101)]
        return {"SampleInt":0.01,"Wavelet":v}
        
        