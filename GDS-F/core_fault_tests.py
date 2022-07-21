# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:28:39 2022

@author: lewthwju
"""

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
from constants import FAULT_0

GeoDataSync=None
IDComparison=None


class FaultTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo
        

      
    def testCreateFault(self):
        faultID=self.repo.createFault(FAULT_0,0)
        self.assertFalse(faultID is None or faultID==0,GDSErr(self.server,"Failed createFault"))
        
    def testGetFaultListAndVerify(self):
        faultID=self.repo.getFaultID(FAULT_0)
        faultIDList=GeoDataSync("getFaultIDList",self.server)
        self.assertFalse(faultIDList==None or faultIDList==0,GDSErr(self.server,"Failed call to getFaultIDList"))
        self.assertTrue(IDInList(IDComparison,faultID,faultIDList),"Failed to find fault in fault list")
        
    def testPutFaultData(self):
        faultID=self.repo.getFaultID(FAULT_0)
        fdata=self.config.getFaultData()
        success=GeoDataSync("putFaultData",self.server,faultID,fdata["sticks"],fdata["points"],fdata["xcoords"],fdata["ycoords"],fdata["zcoords"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed putFaultData"))
        
    def testGetFaultGeom(self):
        faultID=self.repo.getFaultID(FAULT_0)
        knownfdata=self.config.getFaultData()
        fdata=GeoDataSync("getFaultGeom",self.server,faultID)
        self.assertFalse(fdata is None or fdata==0,GDSErr(self.server,"Failed getFaultData"))
        self.assertTrue(compareFloatLists(knownfdata["xcoords"],fdata[b"XCoords"]),"Failed to match XCoords in getFaultGeom")
        self.assertTrue(compareFloatLists(knownfdata["ycoords"],fdata[b"YCoords"]),"Failed to match YCoords in getFaultGeom")
        self.assertTrue(compareFloatLists(knownfdata["zcoords"],fdata[b"ZCoords"]),"Failed to match ZCoords in getFaultGeom")
        
    
        
        
        
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(FaultTestCase(server,repo,config,"testCreateFault"))
        suite.addTest(FaultTestCase(server,repo,config,"testGetFaultListAndVerify"))
        suite.addTest(FaultTestCase(server,repo,config,"testPutFaultData"))
        suite.addTest(FaultTestCase(server,repo,config,"testGetFaultGeom"))
        
        
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
    return FaultTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()