# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:20:14 2022

@author: lewthwju
"""

import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest



from executor import TestExecutor

from test_utils import compareFloatLists    
from test_utils import IDInList
from test_utils import GDSErr 


from constants import SEISMIC_COL_0
from constants import POINTSET_0


GeoDataSync=None
IDComparison=None
 
 



class PointSetTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testCreatePointSet(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        if seisColID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format(SEISMIC_COL_0))
        psID=self.repo.createPointSet(POINTSET_0,seisColID)
        self.assertFalse(psID==None or psID==0,GDSErr(self.server,"Failed createPointSet at top level"))
    
    def testPutPointSetData(self):
        psID=self.repo.getPointSetID(POINTSET_0)
        data=self.config.getPointSetData()
        success=GeoDataSync("putPointSetData",self.server,psID,len(data["XCoords"]),data["XCoords"],data["YCoords"],data["ZCoords"],0)
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to putPointSetData"))
    
    def testGetPointSetData(self):
        psID=self.repo.getPointSetID(POINTSET_0)
        knowndata=self.config.getPointSetData()
        data=GeoDataSync("getPointSetData",self.server,psID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed GDS call to getPointSetData"))
        self.assertTrue(compareFloatLists(data[b"XCoords"],knowndata["XCoords"]),"XCoords do not match in getPointSetData")
        self.assertTrue(compareFloatLists(data[b"YCoords"],knowndata["YCoords"]),"YCoords do not match in getPointSetData")
        self.assertTrue(compareFloatLists(data[b"Values"],knowndata["ZCoords"]),"Values (ZCoords) do not match in getPointSetData")
        
        
 
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(PointSetTestCase(server,repo,config,"testCreatePointSet"))
        suite.addTest(PointSetTestCase(server,repo,config,"testPutPointSetData"))
        suite.addTest(PointSetTestCase(server,repo,config,"testGetPointSetData"))
       
        return suite
    
    
  
def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return PointSetTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    