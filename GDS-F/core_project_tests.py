# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:19:18 2022

@author: lewthwju
"""
import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest

from executor import TestExecutor

from test_utils import IDInList
from test_utils import GDSErr 


from constants import INTERP_COL_0
from constants import INTERP_COL_1
from constants import FOLDER_0
from constants import FOLDER_1


GeoDataSync=None
IDComparison=None




class ProjectTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testGetSystemType(self):
        sysType=GeoDataSync("getSystemType",self.server)
        self.assertFalse(sysType==None or sysType==0,GDSErr(self.server,"Failed GDS call to getSystemType"))
        systemInfo=self.config.getSystemInfo()
        self.assertEqual(str(sysType,"utf-8"),systemInfo["systemType"])
    
    def testGetVersion(self):
        version=GeoDataSync("getVersion",self.server)
        self.assertFalse(version==None or version==0,GDSErr(self.server,"Failed GDS call to getVersion"))
        systemInfo=self.config.getSystemInfo()
        sver=version[b"ServerVersion"]
        cver=version[b"ClientVersion"]
        testcver=systemInfo["clientVersion"]
        testsver=systemInfo["serverVersion"]
        print("Client Version from GDS:{}".format(str(cver,"utf-8")))
        print("Server Version from GDS:{}".format(str(sver,"utf-8")))
        if testcver==None:
            print("No test client version given")
        else:
            self.assertEqual(testcver,str(cver,"utf-8"),"Client version does not match")
        if testsver==None:
            print("No test server version given")
        else:
            self.assertEqual(testsver,str(sver,"utf-8"),"Client version does not match")
            
        
    
    def testGetProjectName(self):
        projName=GeoDataSync("getProjectName",self.server)
        self.assertFalse(projName==None or projName==0,GDSErr(self.server,"Failed GDS call to getProjectName"))
        
    def testGetProjectDirectory(self):
        projDir=GeoDataSync("getProjectDirectory",self.server)
        self.assertFalse(projDir==None or projDir==0,GDSErr(self.server,"Failed GDS call to getProjectDirectory"))
    
    def testCreateSeismicProject(self):
        self.longMessage=False
        success=GeoDataSync("createSeismicProject",self.server)
        self.assertTrue(success,GDSErr(self.server,"Failed GDS call to createSeismicProject"))
        
    def testCreateInterpretationCollectionAtRoot(self):
        args=[0]
        interpID=self.repo.createInterpretationCollection(INTERP_COL_0,*args)
        self.assertFalse(interpID==None or interpID==0,GDSErr(self.server,"Failed GDS call to createInterpretationCollection"))
        
        
    def testCreateInterpretationCollectionInProject(self):
        args=[1]
        interpID=self.repo.createInterpretationCollection(INTERP_COL_1,*args)
        self.assertFalse(interpID==None or interpID==0,GDSErr(self.server,"Failed GDS call to createInterpretationCollection"))
        
    def testGetInterpretationCollectionIDListAndVerify(self):
        interpIDList=GeoDataSync("getInterpretationCollectionIDList",self.server)
        self.assertFalse(interpIDList==None or interpIDList==0,GDSErr(self.server,"Failed call to getInterpretationCollectionIDList"))
        interpID0=self.repo.getInterpretationCollectionID(INTERP_COL_0)
        self.assertTrue(IDInList(IDComparison,interpID0,interpIDList),"Failed to find 'at root' interpretation collection in list")
        interpID1=self.repo.getInterpretationCollectionID(INTERP_COL_1)
        self.assertTrue(IDInList(IDComparison,interpID1,interpIDList),"Failed to find 'in project' interpretation collection in list")
             
    def testCreateFolderInRoot(self):
        folderID=self.repo.createFolder(FOLDER_0)
        self.assertFalse(folderID==None,GDSErr(self.server,"Failed GDS call to createFolder (in root)")) 
        
    def testCreateFolderNested(self):
        args=[self.repo.getFolderID(FOLDER_0)]
        folderID=self.repo.createFolder(FOLDER_1,*args)
        self.assertFalse(folderID==None,GDSErr(self.server,"Failed GDS call to createFolder (nested)"))
        
    def testGetFolderIDListAndVerify(self):
        folderIDList=GeoDataSync("getFolderIDList",self.server)
        self.assertFalse(folderIDList==None or folderIDList==0,GDSErr(self.server,"Failed GDS call to getFolderIDList"))
        folderID0=self.repo.getFolderID(FOLDER_0)
        folderID1=self.repo.getFolderID(FOLDER_1)
        self.assertTrue(IDInList(IDComparison,folderID0,folderIDList),"Failed to find 'in root' folder in list")
        self.assertTrue(IDInList(IDComparison,folderID1,folderIDList),"Failed to find 'nested' folder in list")
        
    def testGetParentID(self):
        parentID=GeoDataSync("getParentID",self.server,self.repo.getFolderID(FOLDER_1))
        self.assertFalse(parentID==None or parentID==0,GDSErr(self.server,"Failed GDS call to getParentID"))
        self.assertEqual(parentID,self.repo.getFolderID(FOLDER_0),"Mismatched IDs for parent folder")
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(ProjectTestCase(server,repo,config,"testGetSystemType"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetVersion"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetProjectName"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetProjectDirectory"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateSeismicProject"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateInterpretationCollectionAtRoot"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateInterpretationCollectionInProject"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetInterpretationCollectionIDListAndVerify"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateFolderInRoot"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateFolderNested"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetFolderIDListAndVerify"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetParentID"))
        
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
    return ProjectTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    