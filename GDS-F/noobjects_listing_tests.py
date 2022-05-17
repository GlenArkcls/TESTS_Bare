# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:28:29 2022

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




GeoDataSync=None
IDComparison=None

class NoObjectsTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo
        

      
    def testGetSeisColIDList(self):
        ret=GeoDataSync("getSeisColIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from getSeisColIDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("project contains no seismic collections!")
        self.assertFalse(find==-1,"Correct error message not shown from getSeisColIDList with empty list: "+err)
        
    def testGet3DSeisIDList(self):
        ret=GeoDataSync("get3DSeisIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from get3DSeisIDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("project contains no Volumes")
        self.assertFalse(find==-1,"Correct error message not shown from get3DSeisIDList with empty list: "+err)
       
    def testGet2DSeisIDList(self):
        ret=GeoDataSync("get2DSeisIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from get2DSeisIDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("project contains no seismic lines!")
        self.assertFalse(find==-1,"Correct error message not shown from get2DSeisIDList with empty list: "+err)
          
    def testGetSurfIDList(self):
        ret=GeoDataSync("getSurfIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from getSurfIDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any surface in this project")
        self.assertFalse(find==-1,"Correct error message not shown from getSurfIDList with empty list: "+err)
        
    def testGet3DHorzIDList(self):
        ret=GeoDataSync("get3DHorzIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from get3DHorzDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any Horizons in this project")
        self.assertFalse(find==-1,"Correct error message not shown from get3DHorzIDList with empty list: "+err)
        
    def testGet2DHorzIDList(self):
        ret=GeoDataSync("get2DHorzIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from get2DHorzDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any 2D horizon in this project")
        self.assertFalse(find==-1,"Correct error message not shown from get2DHorzIDList with empty list: "+err)
        
    def testGetWellIDList(self):
        ret=GeoDataSync("getWellIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from getWellDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any Well in this project")
        self.assertFalse(find==-1,"Correct error message not shown from getWellIDList with empty list: "+err)
        
    def testGetWellCollectionIDList(self):
        ret=GeoDataSync("getWellCollectionIDList",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from getWellCollectionDList that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any Well Collection in")
        self.assertFalse(find==-1,"Correct error message not shown from getWellCollectionIDList with empty list: "+err)
        
    def testGetLogIDListGlobal(self):
        ret=GeoDataSync("getLogIDListGlobal",self.server)
        self.assertTrue(ret==0,GDSErr(self.server,"Returned data from getLogDListGlobal that should be empty"))
        err=GeoDataSync("getLastError",self.server)
        err=str(err,"utf-8")
        find=err.find("Could not find any Well or Log in this project!")
        self.assertFalse(find==-1,"Correct error message not shown from getLogIDListGlobal with empty list: "+err)
        
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGetSeisColIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGet3DSeisIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGet2DSeisIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGetSurfIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGet3DHorzIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGet2DHorzIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGetWellIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGetWellCollectionIDList"))
        suite.addTest(NoObjectsTestCase(server,repo,config,"testGetLogIDListGlobal"))
        
        
        
        return suite
        


def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return NoObjectsTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()