# -*- coding: utf-8 -*-
"""
Contains the definition  of the AssetRepository.
This class contains a mapping from given key namkes to system IDs
It has three sets of methods
createXXX will create an object of type XXX, insert5 it into the repository and return
the system ID
getXXXID returns the system ID of the XXX object given the repo key name
putXXXID puts a system ID into the mapping with a given key - for inserting known
as opposed to created objects
Created on Thu Mar 24 08:33:51 2022

@author: lewthwju
"""
from enum import Enum


GeoDataSync=None

class ObjectType(Enum):
    INTERPRETATION_COLLECTION=1
    FOLDER=2
    SEISMIC_COLLECTION=3
    SEISMIC3D=4
    SEISMIC2D=5
    WAVELET=6
    POINTSET=7
    FAULT=8
    HORIZON=9
    SURFACE=10
    HORIZON_PROPERTY=11
    WELL=12
    WELL_LOG=13
    
    
    
    
class AssetRepository:
    
    def __init__(self):
        
        self.objects={ObjectType.INTERPRETATION_COLLECTION:{},
                      ObjectType.SEISMIC_COLLECTION:{},
                      ObjectType.SEISMIC3D:{},
                      ObjectType.SEISMIC2D:{},
                      ObjectType.FAULT:{},
                      ObjectType.SURFACE:{},
                      ObjectType.POINTSET:{},
                      ObjectType.HORIZON:{},
                      ObjectType.FOLDER:{},
                      ObjectType.HORIZON_PROPERTY:{},
                      ObjectType.WELL:{},
                      ObjectType.WELL_LOG:{}
                      }
    
    def initServer(self,server):
        self.server=server
        
    def createObject(self,createAction,name,*args):
        createdID=GeoDataSync(createAction,self.server,name,*args)
        if createdID==None or createdID==0:
            print(GeoDataSync("getLastError",self.server))
            return False,None
        return True,createdID
        
    '''
    Create Methods - make a new object of the given type with given name
    Object ID is put in repo if success and the ID returned.
    else None is returneds
    '''
      
    def createInterpretationCollection(self,name,*args):
        success,id=self.createObject("createInterpretationCollection",name,*args)
        if success:
            self.objects[ObjectType.INTERPRETATION_COLLECTION][name]=id
        return id
    def createFolder(self,name,*args):
        success,id=self.createObject("createFolder",name,*args)
        if success:
            self.objects[ObjectType.FOLDER][name]=id
        return id
    def createSeismicCollection(self,name):
        success,id=self.createObject("createSeismicCollection",name)
        if success:
            self.objects[ObjectType.SEISMIC_COLLECTION][name]=id
        return id
    def create3DSeismic(self,name,*args):
        success,id=self.createObject("create3DSeis",name,*args)
        if success:
            self.objects[ObjectType.SEISMIC3D][name]=id
        return id
    def create2DSeismic(self,name,*args):
        success,id=self.createObject("create2DSeis",name,*args)
        if success:
            self.objects[ObjectType.SEISMIC2D][name]=id
        return id
    def createSurface(self,name,*args):
        success,id=self.createObject("createSurf",name,*args)
        if success:
            self.objects[ObjectType.SURFACE][name]=id
        return id
    def createHorizon(self,name,*args):
        success,id=self.createObject("create3DHorz",name,*args)
        if success:
            self.objects[ObjectType.HORIZON][name]=id
        return id
    def createHorizonByVolume(self,name,*args):
        success,id=self.createObject("create3DHorzBy3DVolume",name,*args)
        if success:
            self.objects[ObjectType.HORIZON][name]=id
        return id
    def createHorizonProperty(self,hzID,name):
        '''Unfortunatelky need special handling - arguments do not follow pattern
        '''
        createdID=GeoDataSync("create3DHorzProp",self.server,hzID,name)
        if createdID==None or createdID==0:
            print(GeoDataSync("getLastError",self.server))
            return None
        self.objects[ObjectType.HORIZON_PROPERTY][name]=createdID
        return createdID
    def createPointSet(self,name,*args):
        success,id=self.createObject("createPointSet",name,*args)
        if success:
            self.objects[ObjectType.POINTSET][name]=id
        return id
    def createWell(self,name,*args):
        success,id=self.createObject("createWell",name,*args)
        if success:
            self.objects[ObjectType.WELL][name]=id
        return id
    def createWellLog(self,wellID,name):
        '''Unfortunatelky need special handling - arguments do not follow pattern
        '''
        createdID=GeoDataSync("createLog",self.server,wellID,name)
        if createdID==None or createdID==0:
            print(GeoDataSync("getLastError",self.server))
            return None
        self.objects[ObjectType.WELL_LOG][name]=createdID
        return createdID
    def createFault(self,name,*args):
        success,id=self.createObject("createFault",name,*args)
        if success:
            self.objects[ObjectType.FAULT][name]=id
        return id
    '''
    getXXXID Methods
    Retrieve object by name
    '''
    def getFolderID(self,name):
        return self.objects[ObjectType.FOLDER].get(name)
    def get3DSeismicID(self,name):
        return self.objects[ObjectType.SEISMIC3D].get(name)
    def get2DSeismicID(self,name):
        return self.objects[ObjectType.SEISMIC2D].get(name)
    def getSeismicCollectionID(self,name):
        return self.objects[ObjectType.SEISMIC_COLLECTION].get(name)
    def getSurfaceID(self,name):
        return self.objects[ObjectType.SURFACE].get(name)
    def getWaveletID(self,name):
        return self.objects[ObjectType.WAVELET].get(name)
    def getHorizonID(self,name):
        return self.objects[ObjectType.HORIZON].get(name)
    def getHorizonPropertyID(self,name):
        return self.objects[ObjectType.HORIZON_PROPERTY].get(name)
    def getPointSetID(self,name):
        return self.objects[ObjectType.POINTSET].get(name)
    def getWellID(self,name):
        return self.objects[ObjectType.WELL].get(name)
    def getWellLogID(self,name):
        return self.objects[ObjectType.WELL_LOG].get(name)
    def getFaultID(self,name):
        return self.objects[ObjectType.FAULT].get(name)
    
    '''
    putXXXID Methods
    These are for initialising a repo with known names
    if we want to do tests against a known project
    '''
    
    def put3DSeismicID(self,name,ident):
        self.objects[ObjectType.SEISMIC3D][name]=ident
    def put2DSeismicID(self,name,ident):
        self.objects[ObjectType.SEISMIC2D][name]=ident
    def putSeismicCollectionID(self,name,ident):
        self.objects[ObjectType.SEISMIC_COLLECTION][name]=ident
    def putSurfaceID(self,name,ident):
        self.objects[ObjectType.SURFACE][name]=ident
    def putWaveletID(self,name,ident):
        self.objects[ObjectType.WAVELET][name]=ident
    def putHorizonID(self,name,ident):
        self.objects[ObjectType.HORIZON][name]=ident
    def putHorizonPropertyID(self,name,ident):
        self.objects[ObjectType.HORIZON_PROPERTY][name]=ident
    def putPointSetID(self,name,ident):
        self.objects[ObjectType.POINTSET][name]=ident
    def putWellID(self,name,ident):
        self.objects[ObjectType.WELL][name]=ident
    def putWellLogID(self,name,ident):
        self.objects[ObjectType.WELL_LOG][name]=ident
    def putfAULTID(self,name,ident):
        self.objects[ObjectType.FAULT][name]=ident
        
def initModule(geodatasyncFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn