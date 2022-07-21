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

from surfacegeometry import SurfaceGeometry
from seismicgeometry import SeismicGeometry


from constants import SEISMIC3D_0
from constants import SURFACE_0
 
GeoDataSync=None
IDComparison=None

__unittest=True

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
        seisGeom=SeismicGeometry(GeoDataSync("get3DSeisGeom",self.server,seisID))
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
        #print(minIline,maxIline,minXline,maxXline)
        surfGeom=self.config.getSurfGeometry()
        sg=SurfaceGeometry(surfGeom)
        surfVals=self.config.getSurfVals()
        vals=[]
        for i in range(0,sg.getSizeI()):
            for j in range(0,sg.getSizeJ()):
                utm=sg.transformGridCoord([i,j])
                ilxl=seisGeom.transformUTM(utm)
                if ilxl[0]>=minIline and ilxl[0]<=maxIline and ilxl[1]>=minXline and ilxl[1]<=maxXline:
                    #val=surfVals[i*sg.getSizeJ()+j]
                    #print(i,j,val,utm,ilxl)
                    vals.append(surfVals[i*sg.getSizeJ()+j])
        #print("Vals:",vals,len(vals))
        surfVals=GeoDataSync("getSurfValsRangeIlXl",self.server,surfID,seisID,minIline,maxIline,minXline,maxXline)
        #print("Inlines:",surfVals[b"Inlines"])
        #print("XLines:",surfVals[b"Xlines"])
       # print("XCoortds:",surfVals[b"XCoords"])
       # print("YCoords:",surfVals[b"YCoords"])
        #print("SutfVals:",surfVals[b"SurfVals"])
        self.assertFalse(surfVals is None or surfVals==0,GDSErr(self.server,"Failed GDS call to getSurfValsRangeIlXl"))
        #print(len(surfVals[b'Inlines']))
        for i in range(len(surfVals[b'Inlines'])):
             #with self.subTest(i=i):
                 self.assertTrue(surfVals[b'Inlines'][i]>=minIline and surfVals[b'Inlines'][i]<=maxIline,"Returned Inline out of given range from getSurfValsRangeIlXl {}".format(surfVals[b'Inlines'][i]))
                 self.assertTrue(surfVals[b'Xlines'][i]>=minXline and surfVals[b'Xlines'][i]<=maxXline,"Returned Crossline out of given range from getSurfValsRangeIlXl index {}".format(surfVals[b'Xlines'][i]))
        self.assertTrue(compareFloatLists(surfVals[b'SurfVals'],vals),"Mismatched values from getSurfValsRangeIlXl" )
        
    
        
        
 
            
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


def initModule(geodatasyncFn,idCompFn,trace):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    if trace:
        global __unittest
        del(__unittest)
     
     
def getTestSuite(server,repo,config):
    return SurfaceTestCase.getTestSuite(server, repo, config)
  
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    