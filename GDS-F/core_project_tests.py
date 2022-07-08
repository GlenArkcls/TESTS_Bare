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
    
    def testGetVersion(self):
        version=GeoDataSync("getVersion",self.server)
        print(version)
        self.assertFalse(version==None or version==0,GDSErr(self.server,"Failed GDS call to getVersion"))
    
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
        
    def testGetFolderIDList(self):
        folderIDList=GeoDataSync("getFolderIDList",self.server)
        self.assertFalse(folderIDList==None or folderIDList==0,GDSErr(self.server,"Failed GDS call to getFolderIDList"))
        
    def testCreateFolderInRoot(self):
        folderID=self.repo.createFolder(FOLDER_0)
        self.assertFalse(folderID==None,GDSErr(self.server,"Failed GDS call to createFolder (in root)")) 
        
    def testCreateFolderNested(self):
        args=[self.repo.getFolderID(FOLDER_0)]
        folderID=self.repo.createFolder(FOLDER_1,*args)
        self.assertFalse(folderID==None,GDSErr(self.server,"Failed GDS call to createFolder (nested)"))
        
    def testGetParentID(self):
        parentID=GeoDataSync("getParentID",self.server,self.repo.getFolderID(FOLDER_1))
        self.assertFalse(parentID==None or parentID==0,GDSErr(self.server,"Failed GDS call to getParentID"))
        self.assertEqual(parentID,self.repo.getFolderID(FOLDER_0))
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(ProjectTestCase(server,repo,config,"testGetSystemType"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetVersion"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetProjectName"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetProjectDirectory"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateSeismicProject"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateInterpretationCollectionAtRoot"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateInterpretationCollectionInProject"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateFolderInRoot"))
        suite.addTest(ProjectTestCase(server,repo,config,"testCreateFolderNested"))
        suite.addTest(ProjectTestCase(server,repo,config,"testGetParentID"))
        
        return suite
    

def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return ProjectTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    