# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 09:34:16 2022

@author: lewthwju
"""

import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)



import unittest

from test_setup import *
from test_utils import compareFloatLists    
from test_utils import makeCreationGeometryFromFullGeometry 
from test_utils import GDSErr 
from geodatasync.geodatasync import GeoDataSync
#from geodatasync_matlab import GeoDataSync
from asset_repo import AssetRepository



'''
Some constants for the basic test object we make and operate on
'''
SEISMIC_COL_0=b"SeismicCollection0"
SEISMIC_COL_1=b"SeismicCollection1"
SEISMIC3D_0=b"Seismic3D0"
SEISMIC2D_0=b"Seismic2D0"

class SeismicErrorTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,methodName):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
   
    def setUp(self):
        pass
    
    def testCreateSeismicCollection(self):
        seisColID=self.repo.createSeismicCollection(SEISMIC_COL_0)
        self.assertFalse(seisColID==None or seisColID==0,GDSErr(self.server,"Failed to create Seismic Collection:"))
    
    
              
    def testCreate3DSeismic(self):
        args=[self.repo.getSeismicCollectionID(SEISMIC_COL_0)]
        geom=makeCreationGeometryFromFullGeometry(self.config.get3DSeismicGeometry())
        args.extend(list(geom.values()))
        seisID=self.repo.create3DSeismic(SEISMIC3D_0,*args);
        self.assertFalse(seisID==None or seisID==0,GDSErr(self.server,"Failed create3DSeismic"))
    
    def testGet3DSeisValuesSpec_InvalidILXL(self):
        
        seisID=self.repo.get3DSeismicID(b"Seismic3D0")
        if seisID==None:
            self.skipTest("Required 3D Seismic with asset repository name 'Seismic3D0' not found")
        geom=GeoDataSync("get3DSeisGeom",self.server,seisID)
        self.assertFalse(geom==None or geom==0,GDSErr(self.server,"Could not get seismic geometry"))
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=minZ+incZ
        maxZ=maxZ-incZ
        ilines=[-geom[b'MinInline'],geom[b'MinInline']-1]
        xlines=[-geom[b'MinXline'],geom[b'MinXline']-1]
        
        
        gotData=GeoDataSync("get3DSeisTracesSpec",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),ilines,xlines,minZ,maxZ)
        self.assertFalse(gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesSpec"))
        self.assertTrue(gotData[b'NumTraces']==0,"Trace data was returned for invalid IL/XL ranges")
        
    '''
    Put the fidicual data into the cube
    '''
    def testPut3DSeisTraces_InvalidILXL(self):
         geom=self.config.get3DSeismicGeometry()
         ilines,xlines=geom.get3DGeometryILXLPairs()
         ilines=[-il for il in ilines]
         xlines=[-xl for xl in xlines]
         samps=round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1
         volumeData=self.config.get3DSeismicData()
         success=GeoDataSync("put3DSeisTraces",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),volumeData,ilines,xlines,len(ilines),samps,geom[b"MinZ"])
         self.assertFalse(success,GDSErr(self.server,"Succeeded GDS call put3DSeisTrace but with invalid IL/XL"))
         errMsg=GeoDataSync("getLastError",self.server)
         self.assertTrue(errMsg==b'Chosen InLines or CrossLines exceed the boundary of volume!')
        
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
       suite.addTest(SeismicErrorTestCase(server,repo,config,"testCreateSeismicCollection"))
       suite.addTest(SeismicErrorTestCase(server,repo,config,"testCreate3DSeismic"))
       suite.addTest(SeismicErrorTestCase(server,repo,config,"testGet3DSeisValuesSpec_InvalidILXL"))
       suite.addTest(SeismicErrorTestCase(server,repo,config,"testPut3DSeisTraces_InvalidILXL"))
       
       
       return suite
            
    
    

if __name__=="__main__":
    success,server,errmsg=getServer()
   
    try: 
   
   
        print("Server Connected")
        assetRepo=AssetRepository(server)
        if len(sys.argv)>1:
           success,config= setupTest(server,assetRepo,sys.argv[1])
        else:
            success,config=setupTest(server,assetRepo)
        
        print("Test configuration set up:"+errmsg)
        if not success:
            quit();
         
        suite=SeismicErrorTestCase.getTestSuite(server,assetRepo,config)
        
        runner=unittest.TextTestRunner(verbosity=2)
        result=runner.run(suite)
        
        print("Tests Run: "+str(+result.testsRun))
            
        for s in result.failures:
            print(s)
            
        for s in result.errors:
            print(s)
        
    
    except Exception as e:
        print("Exception:"+str(e))
    
      
    
    success,errmsg=releaseServer(server)
    
    print("Server disposal:" + errmsg)