# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:55:37 2022

@author: lewthwju
"""
import test_config
from seismicgeometry import SeismicGeometry
from asset_repo import AssetRepository


'''
These constants are used to put already existing IDs into the asset repo
'''
BOOTSTRAPPED_3DSEISMIC0="Bootstrapped3DSeismic0"
BOOTSTRAPPED_2DSEISMIC0="Bootstrapped2DSesimic0"
BOOTSTRAPPED_SURFACE0="BootstrappedSurface0"
BOOTSTRAPPED_SURFACE0="BootstrappedHorizon0"


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
         seis2DIDList=GeoDataSync("get2DSeisIDList",self.__server)
         self.__repo.put2DSeismicID(BOOTSTRAPPED_2DSEISMIC0,seis2DIDList[0])
#         surfIDList=GeoDataSync("getSurfIDList",self.__server)
#         self.__repo.putSurfaceID(BOOTSTRAPPED_SURFACE0,surfIDList[0])
    
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
            print(self.__surfaceGeom)
        return self.__surfaceGeom
    
     def getSurfVals(self,name=None):
        vals=GeoDataSync("getSurfVals",self.__server,self.__repo.getSurfaceID(BOOTSTRAPPED_SURFACE0))
        return vals[b'SurfVals']
    

def initModule(geodatasyncFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn 