# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:43:43 2022

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


from constants import HORIZON_0
from constants import SEISMIC3D_0
from constants import SEISMIC_COL_0
from constants import HORIZON_PROP_0


GeoDataSync=None
IDComparison=None




class HorizonTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testGet3DHorzIDList(self):
        hzIDList=GeoDataSync("get3DHorzIDList",self.server)
        self.assertFalse(hzIDList==None or hzIDList==0,GDSErr(self.server,"Failed call to get3DHorzIDList"))
    
    def testCreate3DHorizon(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        if seisColID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format(SEISMIC_COL_0))
        #Need to check there is a seismic in the collection otherwise no geometry and cannot add the horizon
        seisIDList=GeoDataSync("get3DSeisIDListCol",self.server,seisColID)
        self.assertFalse(seisIDList==None or seisIDList==0,GDSErr(self.server,"Failed to list seismics from collection"))
        if len(seisIDList)==0:
            self.skipTest("Seismic Collection '{}' has no seismics so no horizon can be added".format(SEISMIC_COL_0))
        args=[0,seisColID]
        hzID=self.repo.createHorizon(HORIZON_0,*args)
        self.assertFalse(hzID==None or hzID==0,GDSErr(self.server,"Failed createHorizon at top level"))
    
    def testGet3DHorzGeometry(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        hzGeom=GeoDataSync("get3DHorzGeom",self.server,hzID)
        self.assertFalse(hzGeom==None or hzGeom==0,GDSErr(self.server,"Failed to retrieve horizon geometry"))
        testGeom=self.config.get3DSeismicGeometry(False)
        hzGeom.pop(b'HorzID')
        for k in hzGeom.keys():
            with self.subTest(k=k):
                self.assertAlmostEqual(hzGeom[k],testGeom[k],4)
        
    def testPut3DHorzValues(self):
        hzVals=self.config.getHorizonVals()
        success=GeoDataSync("put3DHorzValues",self.server,self.repo.getHorizonID(HORIZON_0),hzVals)
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to put3DHorzValues"))
    
    def testGet3DHorzVals(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        ret=GeoDataSync("get3DHorzVals",self.server,hzID)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to get3DHorzVals"))
        self.assertTrue(compareFloatLists(ret[b'HorzVals'],self.config.getHorizonVals()))
        
    def testGet3DHorzValsInXl(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        geom=self.config.get3DSeismicGeometry(False)
        #Set some ranges that are within the cube (unless its really small)
        xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
        loIL=geom.getMinInline()
        hiIL=geom.getMaxInline()
        incIL=geom.getInlineInc()
        hiIL=loIL+incIL
        if hiIL-loIL>7*incIL:
            loIL=loIL+2*incIL
            hiIL=loIL+5*incIL
        elif hiIL-loIL>1*incIL:
            loIL=loIL+1*incIL
            
        loXL=geom.getMinXline()
        hiXL=geom.getMaxXline()
        incXL=geom.getXlineInc()
        hiXL=loXL+incXL
        if hiXL-loXL>3*incXL:
            loIL=loIL+1*incXL
            hiIL=loIL+3*incXL
        
        knownData=self.config.getHorizonVals()
        testVals=[]
        for ilix in range(int((loIL-geom.getMinInline())/geom.getInlineInc()),int((hiIL-geom.getMinInline())/geom.getInlineInc())+1):
            for xlix in range(int((loXL-geom.getMinXline())/geom.getXlineInc()),int((hiXL-geom.getMinXline())/geom.getXlineInc())+1):
                ix=ilix*xlines+xlix
                testVals.append(knownData[int(ix)])
       
        ret=GeoDataSync("get3DHorzValsInXl",self.server,hzID,loIL,hiIL,loXL,hiXL)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to get3DHorzValsInXl"))
        self.assertTrue(compareFloatLists(ret[b'HorzVals'],testVals))
        
        
    def testPut3DHorzValuesSpec(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        geom=self.config.get3DSeismicGeometry(False)
        ilines=list(range(geom.getMinInline(),geom.getMaxInline()+1,geom.getInlineInc()))
        xlines=list(range(geom.getMinXline(),geom.getMaxXline()+1,geom.getXlineInc()))
        ilxls=[[il,xl] for il in ilines for xl in xlines]
        coords=[geom.transformILXL(ilxl) for ilxl in ilxls]
        xcoords=[x[0] for x in coords]
        ycoords=[x[1] for x in coords]
        values=[float(ilxl[0]+ilxl[1]) for ilxl in ilxls]
        ret=GeoDataSync("put3DHorzValuesSpec",self.server,hzID,values,xcoords,ycoords)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to put3DHorzValuesSpec"))
        hzVals=GeoDataSync("get3DHorzVals",self.server,hzID)
        self.assertTrue(compareFloatLists(values,hzVals[b'HorzVals']),GDSErr(self.server,"Failed to recall hz values in put3DHorzValuesSpec"))
        #reset back to original values because we might be doing a comparison of output ??
        self.testPut3DHorzValues()
        
    def testCreate3DHorizonProperty(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        ret=self.repo.createHorizonProperty(hzID,HORIZON_PROP_0)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to create3DHorzProp"))

        
    def testPut3DHorzPropValues(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        propVals=self.config.getHorizonPropertyVals()
        ret=GeoDataSync("put3DHorzPropValues",self.server,hzPropID,propVals)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to put3DHorzPropValues"))
        
    def testGet3DHorzPropVals(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        knownPropVals=self.config.getHorizonPropertyVals()
        propVals=GeoDataSync("get3DHorzPropVals",self.server,hzPropID)
        self.assertFalse(propVals is None or propVals==0,GDSErr(self.server,"Failed call to get3DHorzPropVals"))
        self.assertTrue(compareFloatLists(knownPropVals,propVals[b'PropVals']),GDSErr(self.server,"Hz property values do not match"))
        
    def testGet3DHorzPropValsInXl(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        geom=self.config.get3DSeismicGeometry(False)
        #Set some ranges that are within the cube (unless its really small)
        xlines=(geom.getMaxXline()-geom.getMinXline())/geom.getXlineInc()+1
        loIL=geom.getMinInline()
        hiIL=geom.getMaxInline()
        incIL=geom.getInlineInc()
        hiIL=loIL+incIL
        if hiIL-loIL>7*incIL:
            loIL=loIL+2*incIL
            hiIL=loIL+5*incIL
        elif hiIL-loIL>1*incIL:
            loIL=loIL+1*incIL
         
        loXL=geom.getMinXline()
        hiXL=geom.getMaxXline()
        incXL=geom.getXlineInc()
        hiXL=loXL+incXL
    
        if hiXL-loXL>3*incXL:
            loIL=loIL+1*incXL
            hiIL=loIL+3*incXL
     
        knownData=self.config.getHorizonPropertyVals()
        testVals=[]
        for ilix in range(int((loIL-geom.getMinInline())/geom.getInlineInc()),int((hiIL-geom.getMinInline())/geom.getInlineInc())+1):
            for xlix in range(int((loXL-geom.getMinXline())/geom.getXlineInc()),int((hiXL-geom.getMinXline())/geom.getXlineInc())+1):
                ix=ilix*xlines+xlix
                testVals.append(knownData[int(ix)])
        ret=GeoDataSync("get3DHorzPropValsInXl",self.server,hzPropID,loIL,hiIL,loXL,hiXL)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to get3DHorzPropValsInXl"))
        self.assertTrue(compareFloatLists(ret[b'PropVals'],testVals))
        
        
    def testPut3DHorzPropValuesSpec(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        geom=self.config.get3DSeismicGeometry(False)
        ilines=list(range(geom.getMinInline(),geom.getMaxInline()+1,geom.getInlineInc()))
        xlines=list(range(geom.getMinXline(),geom.getMaxXline()+1,geom.getXlineInc()))
        ilxls=[[il,xl] for il in ilines for xl in xlines]
        coords=[geom.transformILXL(ilxl) for ilxl in ilxls]
        xcoords=[x[0] for x in coords]
        ycoords=[x[1] for x in coords]
        values=[float(ilxl[0]+ilxl[1]) for ilxl in ilxls]
        ret=GeoDataSync("put3DHorzPropValuesSpec",self.server,hzPropID,values,xcoords,ycoords)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to put3DHorzpROPValuesSpec"))
        hzVals=GeoDataSync("get3DHorzPropVals",self.server,hzPropID)
        self.assertTrue(compareFloatLists(values,hzVals[b'PropVals']),GDSErr(self.server,"Failed to recall hz property values in put3DHorzPropValuesSpec"))
        #reset back to original values because we might be doing a comparison of output ??
        self.testPut3DHorzPropValues()
        
        
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizon"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzIDList"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzGeometry"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzValues"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzVals"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzValsInXl"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzValuesSpec"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizonProperty"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzPropValues"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzPropVals"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzPropValsInXl"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzPropValuesSpec"))
        
        return suite
    
    
  
def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return HorizonTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
            
    
    
    