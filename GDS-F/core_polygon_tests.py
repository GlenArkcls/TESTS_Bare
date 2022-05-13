# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:27:46 2022

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



from constants import POLYGON_0


GeoDataSync=None
IDComparison=None
 
 



class PolygonTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testCreatePolygon(self):
        plID=self.repo.createPolygon(POLYGON_0)
        self.assertFalse(plID==None or plID==0,GDSErr(self.server,"Failed createPolygon at top level"))
    
    def testPutPolygonData(self):
        wlID=self.repo.getPolygonID(POLYGON_0)
        data=self.config.getPolygonData()
        success=GeoDataSync("putPolygonData",self.server,wlID,data["Polylines"],data["Points"],data["XCoords"],data["YCoords"],data["ZCoords"],data["IsDepth"],data["Closed"])
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to putPolygonData"))
    
    def testGetPolygonData(self):
        plID=self.repo.getPolygonID(POLYGON_0)
        knowndata=self.config.getPolygonData()
        data=GeoDataSync("getPolygonData",self.server,plID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed GDS call to getPolygonData"))
        self.assertEqual(data[b"NumPolylines"],knowndata["Polylines"],"Number of polylines do not match in getPolygonData")
        self.assertEqual(data[b"Points"],knowndata["Points"],"Number of points do not match in getPolygonData")
        self.assertTrue(compareFloatLists(data[b"XCoords"],knowndata["XCoords"]),"XCoords do not match in getPolygonData")
        self.assertTrue(compareFloatLists(data[b"YCoords"],knowndata["YCoords"]),"YCoords do not match in getPolygonData")
        self.assertTrue(compareFloatLists(data[b"ZCoords"],knowndata["ZCoords"]),"XCoords do not match in getPolygonData")
        self.assertEqual(data[b"isDepth"],knowndata["IsDepth"],"IsDepth does not match in getPolygonData")
       
        
 
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(PolygonTestCase(server,repo,config,"testCreatePolygon"))
        suite.addTest(PolygonTestCase(server,repo,config,"testPutPolygonData"))
        suite.addTest(PolygonTestCase(server,repo,config,"testGetPolygonData"))
       
        return suite
    
    
  
def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return PolygonTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    