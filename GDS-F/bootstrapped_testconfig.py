# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:55:37 2022

@author: lewthwju
"""
import test_config
from seismicgeometry import SeismicGeometry



'''
These constants are used to put already existing IDs into the asset repo
'''
BOOTSTRAPPED_3DSEISMIC0="Bootstrapped3DSeismic0"
BOOTSTRAPPED_2DSEISMIC0="Bootstrapped2DSesimic0"
BOOTSTRAPPED_SURFACE0="BootstrappedSurface0"
BOOTSTRAPPED_HORIZON0="BootstrappedHorizon0"
BOOTSTRAPPED_HORIZONPROP0="BootstrappedHorizon0"
BOOTSTRAPPED_WELL0="BootstrappedWell0"
BOOTSTRAPPED_WELLLOG0="BootstrappedWellLog0"
BOOTSTRAPPED_WELLLOG1="BootstrappedWellLog1"
BOOTSTRAPPED_FAULT0="BootstrappedFault0"
BOOTSTRAPPED_POLYGON0="BootstrappedPolygon0"
BOOTSTRAPPED_POINTSET0="BootstrappedPointSet0"
BOOTSTRAPPED_WAVELET0="BootstrappedWavelet0"


GeoDataSync=None

  


class BootstrappedTestConfig(test_config.TestConfig):
     def __init__(self):
         self.__server=None
         self.__repo=None
         self.__geometry3D=None
         self.__geometry2D=None
         self.__surfaceGeom=None
         
     def initialise(self,server,repo):
         self.__server=server
         self.__repo=repo
         seis3DIDList=GeoDataSync("get3DSeisIDList",self.__server)
         self.__repo.put3DSeismicID(BOOTSTRAPPED_3DSEISMIC0,seis3DIDList[0])
         #seis2DIDList=GeoDataSync("get2DSeisIDList",self.__server)
         #self.__repo.put2DSeismicID(BOOTSTRAPPED_2DSEISMIC0,seis2DIDList[0])
         surfIDList=GeoDataSync("getSurfIDList",self.__server)
         if not surfIDList==0:
             self.__repo.putSurfaceID(BOOTSTRAPPED_SURFACE0,surfIDList[0])
         hz3DIDList=GeoDataSync("get3DHorzIDList",self.__server)
         if not hz3DIDList==0:
             self.__repo.putHorizonID(BOOTSTRAPPED_HORIZON0,hz3DIDList[0])
             hz3DPropIDList=GeoDataSync("get3DHorzPropIDList",self.__server,hz3DIDList[0])
             if not hz3DPropIDList==0:
                 self.__repo.putHorizonPropertyID(BOOTSTRAPPED_HORIZONPROP0,hz3DPropIDList[b'HorzPropIDList'][0])
         wellIDList=GeoDataSync("getWellIDList",self.__server)
         if not wellIDList==0:
             #print(wellIDList[0])
             self.__repo.putWellID(BOOTSTRAPPED_WELL0,wellIDList[0])
             logIDList=GeoDataSync("getLogIDList",self.__server,wellIDList[0])
             if not logIDList==0:
                 #print(logIDList[b'LogIDList'][0])
                 #print(logIDList[b'LogIDList'][1])
                 self.__repo.putWellLogID(BOOTSTRAPPED_WELLLOG0,logIDList[b'LogIDList'][0])
                 self.__repo.putWellLogID(BOOTSTRAPPED_WELLLOG1,logIDList[b'LogIDList'][1])
         psIDList=GeoDataSync("getPointSetIDList",self.__server)
         if not psIDList==0:
             self.__repo.putPointSetID(BOOTSTRAPPED_POINTSET0,psIDList[0])
         polyIDList=GeoDataSync("getPolygonIDList",self.__server)
         if not polyIDList==0:
             self.__repo.putPolygonID(BOOTSTRAPPED_POLYGON0,polyIDList[0])
         faultIDList=GeoDataSync("getFaultIDList",self.__server)
         if not faultIDList==0:
             self.__repo.putFaultID(BOOTSTRAPPED_FAULT0,faultIDList[0])
         waveletIDList=GeoDataSync("getWaveletIDList",self.__server)
         if not waveletIDList==0:
             self.__repo.putWaveletID(BOOTSTRAPPED_WAVELET0,waveletIDList[0])    
        
         
         
    
     def get3DSeismicGeometry(self,name=None):
         if self.__geometry3D==None:
             self.__geometry3D=GeoDataSync("get3DSeisGeom",self.__server,self.__repo.get3DSeismicID(BOOTSTRAPPED_3DSEISMIC0))
             #remove the volumeID
             self.__geometry3D.pop(b"VolID")
         return SeismicGeometry(self.__geometry3D)
    
        
     def get3DSeismicData(self,name=None):
         minZ=self.get3DSeismicGeometry().getMinZ()
         maxZ=self.get3DSeismicGeometry().getMaxZ()
         traces=GeoDataSync("get3DSeisTracesAll",self.__server,self.__repo.get3DSeismicID(BOOTSTRAPPED_3DSEISMIC0),minZ,maxZ)
         return traces[b'Traces']
    
     def get2DSeismicGeometry(self,name=None):
         if self.__geometry2D==None:
             geom=GeoDataSync("get2DSeisGeom",self.__server,self.__repo.get2DSeismicID(BOOTSTRAPPED_2DSEISMIC0))
             self.__geometry2D={b'isDepth': geom[b'isDepth'],
                                 b'XCoords': geom[b'XCoords'],
                                 b'YCoords': geom[b'YCoords'], 
                                 b'TraceLength':round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1,
                                 b'MinZ':geom[b'MinZ'],
                                 b'ZInc':geom[b'ZInc']}
         return self.__geometry2D 
    
     def get2DLineData(self,name=None):
         gotData=GeoDataSync("get2DSeisTracesAll",self.__server,self.__repo.get2DSeismicID(BOOTSTRAPPED_2DSEISMIC0))
         return gotData[b'Traces']
        
   
     def getSurfGeometry(self,name=None):
        if self.__surfaceGeom==None:
            self.__surfaceGeom=GeoDataSync("getSurfGeom",self.__server,self.__repo.getSurfaceID(BOOTSTRAPPED_SURFACE0))
            self.__surfaceGeom.pop(b'SurfID')
        return self.__surfaceGeom
    
     def getSurfVals(self,name=None):
        vals=GeoDataSync("getSurfVals",self.__server,self.__repo.getSurfaceID(BOOTSTRAPPED_SURFACE0))
        return vals[b'SurfVals']
    
     def getHorizonVals(self,name=None):
        vals=GeoDataSync("get3DHorzVals",self.__server,self.__repo.getHorizonID(BOOTSTRAPPED_HORIZON0))
        return vals[b'HorzVals']
    
     def getHorizonPropertyVals(self,name=None):
        vals=GeoDataSync("get3DHorzPropVals",self.__server,self.__repo.getHorizonPropertyID(BOOTSTRAPPED_HORIZONPROP0))
        return vals[b'PropVals']
    
     def getWellHeadCoordinates(self,name=None):
        info=GeoDataSync("getWellInfo",self.__server,self.__repo.getWellID(BOOTSTRAPPED_WELL0))
        return [info[b'XCoord'],info[b'YCoord']]
    
     def getWellTrack(self,name=None):
        track=GeoDataSync("getWellGeom",self.__server,self.__repo.getWellID(BOOTSTRAPPED_WELL0))
        info=GeoDataSync("getWellInfo",self.__server,self.__repo.getWellID(BOOTSTRAPPED_WELL0))
        return {"X":track[b'XCoords'],"Y":track[b'YCoords'],"Z":track[b'ZCoords'],"reftype":info[b'ReferenceLevelType'],"reflevel":info[b'ReferenceLevel']}
    
     def getWellLogData(self,param=0):
        if param==0:
            log=GeoDataSync("getLogData",self.__server,self.__repo.getWellLogID(BOOTSTRAPPED_WELLLOG0))
        else:
            log=GeoDataSync("getLogData",self.__server,self.__repo.getWellLogID(BOOTSTRAPPED_WELLLOG1))
        return {"Values":log[b'LogVals'],"Start":log[b'TimeVals'][0],"Interval":log[b'TimeVals'][1]-log[b'TimeVals'][0]}
   
   
     def getFaultData(self,name=None):
        fdata=GeoDataSync("getFaultGeom",self.__server,self.__repo.getFaultID(BOOTSTRAPPED_FAULT0))
        retdata={"sticks":fdata[b'NumSticks'],"points":fdata[b'PointsPerStick'],"xcoords":fdata[b'XCoords'],"ycoords":fdata[b'YCoords'],"zcoords":fdata[b'ZCoords']}
        return retdata
    
     def getPointSetData(self,isDepth=False):
         psdata=GeoDataSync("getPointSetData",self.__server,self.__repo.getPointSetID(BOOTSTRAPPED_POINTSET0))
         return {"XCoords":psdata[b'XCoords'],"YCoords":psdata[b'YCoords'],"ZCoords":psdata[b'Values'],"isDepth":psdata[b'isDepth']}
    
     def getWaveletData(self,name=None):
         wdata=GeoDataSync("getWaveletData",self.__server,self.__repo.getWaveletID(BOOTSTRAPPED_WAVELET0))
         return {"SampleInt":wdata[b'SampleInterval'],"Wavelet":wdata[b'Data']}
    
     def getPolygonData(self,isDepth=False):
         pdata=GeoDataSync("getPolygonData",self.__server,self.__repo.getPolygonID(BOOTSTRAPPED_POLYGON0))
         return {"Polylines":pdata[b'NumPolylines'],"Points":pdata[b'Points'],"XCoords":pdata[b'XCoords'],"YCoords":pdata[b'YCoords'],"ZCoords":pdata[b'ZCoords'],"IsDepth":pdata[b'isDepth'],"Closed":[0]*(pdata[b'NumPolylines'])}
       
    

def initModule(geodatasyncFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn 