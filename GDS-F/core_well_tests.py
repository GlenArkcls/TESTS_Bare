# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:48:57 2022

@author: lewthwju
"""

import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest


from executor import TestExecutor


from test_utils import GDSErr 
from test_utils import compareFloatLists
from test_utils import IDInList


from constants import WELL_0
from constants import WELL_LOG_0
from constants import WELL_LOG_1



GeoDataSync=None
IDComparison=None

class WellTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo
        
    def testCreateWellRoot(self):
        success=GeoDataSync("createWellRoot",self.server)
        self.assertFalse(success==0,GDSErr(self.server,"Failed createWellRoot"))
      
    def testCreateWell(self):
        wellID=self.repo.createWell(WELL_0)
        self.assertFalse(wellID is None or wellID==0,GDSErr(self.server,"Failed createWell"))
        
    def testPutWellHead(self):
        wellID=self.repo.getWellID(WELL_0)
        headCoords=self.config.getWellHeadCoordinates()
        success=GeoDataSync("putWellHead",self.server,wellID,headCoords[0],headCoords[1])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellHead"))
        
    def testPutWellTrack(self):
        wellID=self.repo.getWellID(WELL_0)
        track=self.config.getWellTrack()
        success=GeoDataSync("putWellTrack",self.server,wellID,track["X"],track["Y"],track["Z"],track["reftype"],track["reflevel"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellTrack"))
        
    def testCreateWellLog(self):
        wellID=self.repo.getWellID(WELL_0)
        logID=self.repo.createWellLog(wellID,WELL_LOG_0)
        self.assertFalse(logID is None,GDSErr(self.server,"Failed createLog"))
        logID=self.repo.createWellLog(wellID,WELL_LOG_1)
        self.assertFalse(logID is None,GDSErr(self.server,"Failed createLog"))
        
    def testPutLogData(self):
        logID=self.repo.getWellLogID(WELL_LOG_0)
        log=self.config.getWellLogData0()
        success=GeoDataSync("putLogData",self.server,logID,log["Values"],log["Start"],log["Interval"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putLogData"))
        logID=self.repo.getWellLogID(WELL_LOG_1)
        log=self.config.getWellLogData1()
        success=GeoDataSync("putLogData",self.server,logID,log["Values"],log["Start"],log["Interval"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putLogData"))
        
    def testGetLogData(self):
        logID=self.repo.getWellLogID(WELL_LOG_0)
        log=self.config.getWellLogData0()
        logData=GeoDataSync("getLogData",self.server,logID)
        self.assertFalse(logData is None or logData==0,GDSErr(self.server,"Failed getLogData"))
        self.assertTrue(compareFloatLists(log["Values"],logData[b"LogVals"]))
        
    def testGetWellGeom(self):
        wellID=self.repo.getWellID(WELL_0)
        knowntrack=self.config.getWellTrack()
        track=GeoDataSync("getWellGeom",self.server,wellID)
        self.assertFalse(track is None or track==0,GDSErr(self.server,"Failed getWellGeom"))
        self.assertTrue(compareFloatLists(knowntrack["X"],track[b"XCoords"]),"Well track X coords do not match")
        self.assertTrue(compareFloatLists(knowntrack["Y"],track[b"YCoords"]),"Well track Y coords do not match")
        self.assertTrue(compareFloatLists(knowntrack["Z"],track[b"ZCoords"]),"Well track Z coords do not match")
        
    def testGetWellTrajectory(self):
        wellID=self.repo.getWellID(WELL_0)
        knowntrack=self.config.getWellTrack()
        track=GeoDataSync("getWellTrajectory",self.server,wellID)
        self.assertFalse(track is None or track==0,GDSErr(self.server,"Failed getWellTrajectory"))
        self.assertTrue(compareFloatLists(knowntrack["X"],track[b"XCoords"]),"Well trajectory X coords do not match")
        self.assertTrue(compareFloatLists(knowntrack["Y"],track[b"YCoords"]),"Well trajectory Y coords do not match")
        self.assertTrue(compareFloatLists(knowntrack["Z"],track[b"ZCoords"]),"Well trajectory Z coords do not match")
        
    def testGetWellData(self):
        wellID=self.repo.getWellID(WELL_0)
        data0=self.config.getWellLogData0()
        data1=self.config.getWellLogData1()
        data=GeoDataSync("getWellData",self.server,wellID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed getWellData"))
        idList=data[b'LogIDs']
        self.assertTrue(IDInList(IDComparison,self.repo.getWellLogID(WELL_LOG_0),idList),"Well log not in ID list in getWellData")
        self.assertTrue(IDInList(IDComparison,self.repo.getWellLogID(WELL_LOG_1),idList),"Well log not in ID list in getWellData")
        for i in range(0,len(idList)):
            if IDComparison(idList[i],self.repo.getWellLogID(WELL_LOG_0)):
                self.assertTrue(compareFloatLists(data0["Values"],data[b"LogVals"][i]),"Well log data does not match")    
            elif IDComparison(idList[i],self.repo.getWellLogID(WELL_LOG_1)):
                self.assertTrue(compareFloatLists(data1["Values"],data[b"LogVals"][i]),"Well log data does not match") 
        
        
        
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellRoot"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWell"))
        suite.addTest(WellTestCase(server,repo,config,"testPutWellHead"))
        suite.addTest(WellTestCase(server,repo,config,"testPutWellTrack"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellLog"))
        suite.addTest(WellTestCase(server,repo,config,"testPutLogData"))
        suite.addTest(WellTestCase(server,repo,config,"testGetLogData"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellGeom"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellTrajectory"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellData"))
        
        return suite
        


def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return WellTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()