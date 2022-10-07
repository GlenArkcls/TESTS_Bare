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
from constants import WELL_1
from constants import WELL_COLLECTION_0
from constants import WELL_LOG_0
from constants import WELL_LOG_1
from constants import WELL_LOG_2
from constants import WELL_LOG_3
from constants import WELL_LOG_4
from constants import GLOBAL_LOG_0
from constants import WELL_MARKER_0
from constants import COLORMAP_0
from constants import LOG_TEMPLATE_0
from constants import LOG_TEMPLATE_1

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
        self.assertFalse(success==None or success==0,GDSErr(self.server,"Failed createWellRoot"))
        
    def testCreateWellCollection(self):
        wellID=self.repo.createWellCollection(WELL_COLLECTION_0)
        self.assertFalse(wellID is None or wellID==0,GDSErr(self.server,"Failed createWellCollection"))
      
    def testCreateWell(self):
        wellID=self.repo.createWell(WELL_0)
        self.assertFalse(wellID is None or wellID==0,GDSErr(self.server,"Failed createWell"))
        
    def testCreateWellInCollection(self):
        wellColID=self.repo.getWellCollectionID(WELL_COLLECTION_0)
        wellID1=self.repo.createWell(WELL_1,wellColID)
        self.assertFalse(wellID1 is None or wellID1==0,GDSErr(self.server,"Failed createWell in collection"))
        
    def testGetWellListAndVerify(self):
        wellIDList=GeoDataSync("getWellIDList",self.server)
        self.assertFalse(wellIDList==None or wellIDList==0,GDSErr(self.server,"Failed call to getWellIDList"))
        wellID=self.repo.getWellID(WELL_0)
        self.assertTrue(IDInList(IDComparison,wellID,wellIDList))
    
    
        
    def testGetWellCollectionListAndVerify(self):
        wellColIDList=GeoDataSync("getWellCollectionIDList",self.server)
        self.assertFalse(wellColIDList==None or wellColIDList==0,GDSErr(self.server,"Failed call to getWellCollectionIDList"))
        wellColID=self.repo.getWellCollectionID(WELL_COLLECTION_0)
        self.assertTrue(IDInList(IDComparison,wellColID,wellColIDList))
        
    def testPutWellHead(self):
        wellID=self.repo.getWellID(WELL_0)
        headCoords=self.config.getWellHeadCoordinates()
        success=GeoDataSync("putWellHead",self.server,wellID,headCoords[0],headCoords[1])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellHead"))
        wellID1=self.repo.getWellID(WELL_1)
        headCoords=self.config.getWellHeadCoordinates()
        success=GeoDataSync("putWellHead",self.server,wellID1,headCoords[0],headCoords[1])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellHead"))
        
    def testPutWellTrack(self):
        wellID=self.repo.getWellID(WELL_0)
        track=self.config.getWellTrack()
        success=GeoDataSync("putWellTrack",self.server,wellID,track["X"],track["Y"],track["Z"],track["reftype"],track["reflevel"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellTrack"))
    
    def testPutWellTrackWithoutOptions(self):
        wellID=self.repo.getWellID(WELL_1)
        track=self.config.getWellTrack()
        success=GeoDataSync("putWellTrack",self.server,wellID,track["X"],track["Y"],track["Z"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putWellTrack missing opt args"))
        
    def testCreateWellLog(self):
        wellID=self.repo.getWellID(WELL_0)
        logID=self.repo.createWellLog(wellID,WELL_LOG_0)
        self.assertFalse(logID is None or logID==0,GDSErr(self.server,"Failed createLog"))
        logID=self.repo.createWellLog(wellID,WELL_LOG_1)
        self.assertFalse(logID is None or logID==0,GDSErr(self.server,"Failed createLog"))
        logID=self.repo.createWellLog(wellID,WELL_LOG_2)
        self.assertFalse(logID is None or logID==0,GDSErr(self.server,"Failed createLog"))
        
    def testGetLogListAndVerify(self):
        wellID=self.repo.getWellID(WELL_0)
        logIDList=GeoDataSync("getLogIDList",self.server,wellID)
        self.assertFalse(logIDList is None or logIDList==0,GDSErr(self.server,"Failed getLogIDList"))
        log0ID=self.repo.getWellLogID(WELL_LOG_0)
        log1ID=self.repo.getWellLogID(WELL_LOG_1)
        log2ID=self.repo.getWellLogID(WELL_LOG_2)
        self.assertTrue(IDComparison(wellID,logIDList[b"WellID"]),"Incorrect wellID from getLogIDList")
        self.assertTrue(IDInList(IDComparison,log0ID,logIDList[b"LogIDList"]),"Created log not on list")
        self.assertTrue(IDInList(IDComparison,log1ID,logIDList[b"LogIDList"]),"Created log not on list")
        self.assertTrue(IDInList(IDComparison,log2ID,logIDList[b"LogIDList"]),"Created log not on list")
        
        
    def testPutLogData(self):
        logID=self.repo.getWellLogID(WELL_LOG_0)
        log=self.config.getWellLogData(0)
        success=GeoDataSync("putLogData",self.server,logID,log["Values"],log["Start"],log["Interval"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putLogData"))
        logID=self.repo.getWellLogID(WELL_LOG_1)
        log=self.config.getWellLogData(1)
        success=GeoDataSync("putLogData",self.server,logID,log["Values"],log["Start"],log["Interval"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putLogData"))
        
      
    def testGetLogDataRange(self):
        logID=self.repo.getWellLogID(WELL_LOG_0)
        log=self.config.getWellLogData(0)
        minv=min(log["Values"])
        maxv=max(log["Values"])
        ret=GeoDataSync("getLogDataRange",self.server,logID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed getLogDataRange"))
        self.assertTrue(minv==ret[b'MinValue'],"Mismatched min value in getLogDataRange")
        self.assertTrue(maxv==ret[b'MaxValue'],"Mismatched max value in getLogDataRange")
        
    def testGetLogData(self):
        logID=self.repo.getWellLogID(WELL_LOG_0)
        log=self.config.getWellLogData(0)
        logData=GeoDataSync("getLogData",self.server,logID)
        self.assertFalse(logData is None or logData==0,GDSErr(self.server,"Failed getLogData"))
        self.assertTrue(compareFloatLists(log["Values"],logData[b"LogVals"]))
        logID=self.repo.getWellLogID(WELL_LOG_1)
        log=self.config.getWellLogData(1)
        logData=GeoDataSync("getLogData",self.server,logID)
        self.assertFalse(logData is None or logData==0,GDSErr(self.server,"Failed getLogData"))
        self.assertTrue(compareFloatLists(log["Values"],logData[b"LogVals"]))
        
    def testPutLogDataExplicit(self):
        logID=self.repo.getWellLogID(WELL_LOG_2)
        log=self.config.getWellLogData(2)
        start=log["Start"]
        intr=log["Interval"]
        nvals=len(log["Values"])
        depths=[float(start) + i*intr for i in range(0,nvals)]
        success=GeoDataSync("putLogDataExplicit",self.server,logID,depths,log["Values"])
        self.assertFalse(success==0 or success==None,GDSErr(self.server,"Failed putLogDataExplicit"))
        logData=GeoDataSync("getLogData",self.server,logID)
        self.assertFalse(logData is None or logData==0,GDSErr(self.server,"Failed getLogData"))
        self.assertTrue(compareFloatLists(log["Values"],logData[b"LogVals"]))
    
    def testChangeLogColormap(self):
        cmID=self.repo.getColormapID(COLORMAP_0)
        if cmID==None:
            self.skipTest("No Colormap ID avaialbale")
        logID=self.repo.getWellLogID(WELL_LOG_0)
        ret=GeoDataSync("changeLogColormap",self.server,logID,cmID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to changeLogColormap"))
        
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
        data0=self.config.getWellLogData(0)
        data1=self.config.getWellLogData(1)
        data=GeoDataSync("getWellData",self.server,wellID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed getWellData"))
        idList=data[b'LogIDs']
        self.assertTrue(IDInList(IDComparison,self.repo.getWellLogID(WELL_LOG_0),idList),"Well log 0 not in ID list in getWellData")
        self.assertTrue(IDInList(IDComparison,self.repo.getWellLogID(WELL_LOG_1),idList),"Well log 1 not in ID list in getWellData")
        for i in range(0,len(idList)):
            if IDComparison(idList[i],self.repo.getWellLogID(WELL_LOG_0)):
                self.assertTrue(compareFloatLists(data0["Values"],data[b"LogVals"][i]),"Well log 0 data does not match")    
            elif IDComparison(idList[i],self.repo.getWellLogID(WELL_LOG_1)):
                self.assertTrue(compareFloatLists(data1["Values"],data[b"LogVals"][i]),"Well log 1 data does not match") 
        
    def testGetWellInfo(self):
        wellID=self.repo.getWellID(WELL_0)
        info=GeoDataSync("getWellInfo",self.server,wellID)
        self.assertFalse(info==None or info==0,GDSErr(self.server,"Failed call to getWellInfo"))
    
    def testCreateLogTemplate(self):
        wellID=self.repo.getWellID(WELL_0)
        logID=self.repo.createLogTemplate(wellID,WELL_LOG_3)
        self.assertFalse(logID==None or logID==0,GDSErr(self.server,"Failed call to createLogTemplate"))
        
   
    def testGetTemplateCategoryIDList(self):
        catIDs=GeoDataSync("getTemplateCategoryIDList",self.server)
        self.assertFalse(catIDs==None or catIDs==0,GDSErr(self.server,"Failed call to  getTemplateCategoryIDList"))
        
    def testGetTemplateCategoryIDList(self):
        catIDs=GeoDataSync("getTemplateCategoryIDList",self.server)
        self.assertFalse(catIDs==None or catIDs==0,GDSErr(self.server,"Failed call to  getTemplateCategoryIDList"))
        
        
    def testGetTemplateInCategoryIDList(self):
        catIDs=GeoDataSync("getTemplateCategoryIDList",self.server)
        if catIDs==None or catIDs==0:
            self.skipTest("No Template categories available")
        tempIDs=GeoDataSync("getTemplateIDList",self.server,catIDs[0])
        self.assertFalse(tempIDs==None or tempIDs==0,GDSErr(self.server,"Failed call to  getTemplatesIDList in category"))
        self.repo.putLogTemplateID(LOG_TEMPLATE_0,tempIDs[0])
        
    def testCreateLogFromTemplate(self):
        wellID=self.repo.getWellID(WELL_0)
        pid=self.repo.getLogTemplateID(LOG_TEMPLATE_0)
        if pid==None:
            self.skipTest("No Log Template ID available")
        logID=self.repo.createLogTemplate(wellID,WELL_LOG_4,pid)
        self.assertFalse(logID==None or logID==0,GDSErr(self.server,"Failed call to  createLogTemplate from tewmplate"))
        
        
    def testCreateGlobalLog(self):
        logID=self.repo.createGlobalLog(GLOBAL_LOG_0)
        self.assertFalse(logID==None or logID==0,GDSErr(self.server,"Failed call to createGlobalLog"))
        
    def testGetGlobalLogListAndVerify(self):
        logID=self.repo.getGlobalLogID(GLOBAL_LOG_0)
        logIDList=GeoDataSync("getLogIDListGlobal",self.server)
        self.assertFalse(logIDList==None or logIDList==0,GDSErr(self.server,"Failed call to getLogIDListGlobal"))
        self.assertTrue(IDInList(IDComparison,logID,logIDList[b"LogIDList"]),"Global Log ID not found in ID list")
        
    def testCreateWellMarker(self):
        wellID=self.repo.getWellID(WELL_0)
        args=[500.0,0]
        mkID=self.repo.createWellMarker(wellID,WELL_MARKER_0,*args)
        self.assertFalse(mkID==None or mkID==0,GDSErr(self.server,"Failed call to createWellMarker"))
        
    def testGetWellMarkersAndVerify(self):
        wellID=self.repo.getWellID(WELL_0)
        mkID=self.repo.getWellMarkerID(WELL_MARKER_0)
        mkIDList=GeoDataSync("getWellMarkers",self.server,wellID)
        self.assertFalse(mkIDList==None or mkIDList==0,GDSErr(self.server,"Failed call to getWellMarkers"))
        self.assertTrue(IDInList(IDComparison,mkID,mkIDList[b'MarkerIDs']),"Failed to find marker ID in list")
        
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellRoot"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellCollection"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWell"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellInCollection"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellListAndVerify"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellCollectionListAndVerify"))
        suite.addTest(WellTestCase(server,repo,config,"testPutWellHead"))
        suite.addTest(WellTestCase(server,repo,config,"testPutWellTrack"))
        suite.addTest(WellTestCase(server,repo,config,"testPutWellTrackWithoutOptions"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellLog"))
        suite.addTest(WellTestCase(server,repo,config,"testGetLogListAndVerify"))
        suite.addTest(WellTestCase(server,repo,config,"testPutLogData"))
        suite.addTest(WellTestCase(server,repo,config,"testGetLogData"))
        suite.addTest(WellTestCase(server,repo,config,"testPutLogDataExplicit"))
        suite.addTest(WellTestCase(server,repo,config,"testChangeLogColormap"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellGeom"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellTrajectory"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellData"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellInfo"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateLogTemplate"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateGlobalLog"))
        suite.addTest(WellTestCase(server,repo,config,"testGetGlobalLogListAndVerify"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateWellMarker"))
        suite.addTest(WellTestCase(server,repo,config,"testGetWellMarkersAndVerify"))
        suite.addTest(WellTestCase(server,repo,config,"testGetTemplateCategoryIDList"))
        suite.addTest(WellTestCase(server,repo,config,"testGetTemplateInCategoryIDList"))
        suite.addTest(WellTestCase(server,repo,config,"testCreateLogFromTemplate"))
        
        return suite
        


def initModule(geodatasyncFn,idCompFn,trace):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    if not trace:
        global __unittest
        __unittest=True
    
def getTestSuite(server,repo,config):
    return WellTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()