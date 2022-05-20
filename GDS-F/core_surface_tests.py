# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:01:55 2022

@author: lewthwju
"""

import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest


from executor import TestExecutor

from test_utils import compareFloatLists    
from test_utils import GDSErr 
from test_utils import IDInList


from constants import SEISMIC3D_0
from constants import SURFACE_0
 
GeoDataSync=None
IDComparison=None



class SurfaceTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testCreateTopLevelSurface(self):
        args=[0]
        geom=self.config.getSurfGeometry()
        args.extend(list(geom.values()))
        surfID=self.repo.createSurface(SURFACE_0,*args)
        self.assertFalse(surfID==None or surfID==0,GDSErr(self.server,"Failed createSurface at top level"))
        
    def testGetSurfIDList(self):
        surfIDList=GeoDataSync("getSurfIDList",self.server)
        self.assertFalse(surfIDList==0 or surfIDList==None,GDSErr(self.server,"Failed call to getSurfIDList"))
        surfID=self.repo.getSurfaceID(SURFACE_0)
        self.assertTrue(IDInList(IDComparison,surfID,surfIDList),"Created surface ID not found in list from getSurfIDList")
    
    def testGetSurfGeom(self):
        surfGeom=GeoDataSync("getSurfGeom",self.server,self.repo.getSurfaceID(SURFACE_0))
        self.assertFalse(surfGeom==None or surfGeom==0,GDSErr(self.server,"Failed GDS call to getSurfGeom"))
        fidgeom=self.config.getSurfGeometry()
        for k in list(fidgeom.keys()):
            with self.subTest(k=k):
                self.assertAlmostEqual(surfGeom[k],fidgeom[k],4,"Failed geometry comparison")
    
    def testPutSurfVals(self):
        surfVals=self.config.getSurfVals()
        surfID=self.repo.getSurfaceID(SURFACE_0)
        success=GeoDataSync("putSurfVals",self.server,surfID,surfVals)
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to putSurfVals"))
        
    def testGetSurfDataRange(self):
        surfID=self.repo.getSurfaceID(SURFACE_0)
        surfVals=self.config.getSurfVals()
        minv=min(surfVals)
        maxv=max(surfVals)
        minmax=GeoDataSync("getSurfDataRange",self.server,surfID)
        self.assertFalse(minmax is None or minmax==0,GDSErr(self.server,"Failed GDS call to getSurfDataRange"))
        self.assertAlmostEqual(minv,minmax[b'MinValue'],4,"Mismatched min value in getSurfDataRange")
        self.assertAlmostEqual(maxv,minmax[b'MaxValue'],4,"Mismatched max value in getSurfDataRange")
    
    def testGetSurfVals(self):
        surfID=self.repo.getSurfaceID(SURFACE_0)
        surfVals=self.config.getSurfVals()
        data=GeoDataSync("getSurfVals",self.server,surfID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed GDS call to getSurfVals"))
        self.assertTrue(compareFloatLists(data[b"SurfVals"],surfVals),"retreived surface data does not match")
    
    
    def testGetSurfValsRangeIlXl(self):
        surfID=self.repo.getSurfaceID(SURFACE_0)
        seisID=self.repo.get3DSeismicID(SEISMIC3D_0)
        if seisID==None:
            self.skipTest("Required 3D Seismic with asset repository name '{}' not found".format(SEISMIC3D_0))
        seisGeom=GeoDataSync("get3DSeisGeom",self.server,seisID)
        self.assertFalse(seisGeom is None or seisGeom==0,GDSErr(self.server,"Could not get seismic geometry"))
        deltaIL=seisGeom[b'MaxInline']-seisGeom[b'MinInline']
        deltaXL=seisGeom[b'MaxXline']-seisGeom[b'MinXline']
        if deltaIL>7:
            deltaIL=2
        elif deltaIL>5:
            deltaIL=1
        else:
            deltaIL=0
        if deltaXL>7:
                deltaXL=2
        elif deltaXL>5:
              deltaXL=1
        else:
            deltaIL=0
        minIline=seisGeom[b'MinInline']+deltaIL
        maxIline=seisGeom[b'MaxInline']-deltaIL
        minXline=seisGeom[b'MinXline']+deltaXL
        maxXline=seisGeom[b'MaxXline']-deltaXL
        
        surfVals=GeoDataSync("getSurfValsRangeIlXl",self.server,surfID,seisID,minIline,maxIline,minXline,maxXline)
        self.assertFalse(surfVals is None or surfVals==0,GDSErr(self.server,"Failed GDS call to getSurfValsRangeIlXl"))
        for i in range(len(surfVals[b'Inlines'])):
             with self.subTest(i=i):
                 self.assertTrue(surfVals[b'Inlines'][i]>=minIline and surfVals[b'Inlines'][i]<=maxIline,"Returned Inline out of given range from getSurfValsRangeIlXl")
                 self.assertTrue(surfVals[b'Xlines'][i]>=minXline and surfVals[b'Xlines'][i]<=maxXline,"Returned Crossline out of given range from getSurfValsRangeIlXl")
        self.assertTrue(compareFloatLists(surfVals[b'SurfVals'],self.config.getSurfVals()))
        
    
        
        
 
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(SurfaceTestCase(server,repo,config,"testCreateTopLevelSurface"))
        suite.addTest(SurfaceTestCase(server,repo,config,"testGetSurfGeom"))
        suite.addTest(SurfaceTestCase(server,repo,config,"testGetSurfIDList"))
        
        suite.addTest(SurfaceTestCase(server,repo,config,"testPutSurfVals"))
        suite.addTest(SurfaceTestCase(server,repo,config,"testGetSurfDataRange"))
        suite.addTest(SurfaceTestCase(server,repo,config,"testGetSurfVals"))
        suite.addTest(SurfaceTestCase(server,repo,config,"testGetSurfValsRangeIlXl"))
        return suite


def initModule(geodatasyncFn,idCompFn):
     global GeoDataSync
     GeoDataSync=geodatasyncFn
     global IDComparison
     IDComparison=idCompFn
     
     
def getTestSuite(server,repo,config):
    return SurfaceTestCase.getTestSuite(server, repo, config)
  
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    