# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:43:43 2022

@author: lewthwju
"""

import os
import sys
import math


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest


from executor import TestExecutor


from test_utils import GDSErr 
from test_utils import compareFloatLists
from test_utils import IDInList


from constants import HORIZON_0
from constants import HORIZON_1
from constants import HORIZON_2
from constants import HORIZON_3
from constants import HORIZON2D_0
from constants import HORIZON2D_1
from constants import SEISMIC3D_0
from constants import SEISMIC2D_0
from constants import SEISMIC_COL_0
from constants import SEISMIC_COL_1
from constants import HORIZON_PROP_0
from constants import INTERP_COL_0
from constants import COLORMAP_0


GeoDataSync=None
IDComparison=None



class HorizonTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    
    
    def testCreate3DHorizon(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        if seisColID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format("SEISMIC_COL_0"))
        #Need to check there is a seismic in the collection otherwise no geometry and cannot add the horizon
        seisIDList=GeoDataSync("get3DSeisIDListCol",self.server,seisColID)
        self.assertFalse(seisIDList==None or seisIDList==0,GDSErr(self.server,"Failed to list seismics from collection"))
        if len(seisIDList)==0:
            self.skipTest("Seismic Collection '{}' has no seismics so no horizon can be added".format("SEISMIC_COL_0"))
        args=[0,seisColID]
        hzID=self.repo.createHorizon(HORIZON_0,*args)
        self.assertFalse(hzID==None or hzID==0,GDSErr(self.server,"Failed createHorizon at top level"))
    
    def testCreate3DHorizonBy3DVolume(self):
        seisID=self.repo.get3DSeismicID(SEISMIC3D_0)
        if seisID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format("SEISMIC3D_0"))  
        args=[0,seisID]
        hzID=self.repo.createHorizonByVolume(HORIZON_1,*args)
        self.assertFalse(hzID==None or hzID==0,GDSErr(self.server,"Failed createHorizonBy3DVolume at top level"))
        
    def testCreate3DHorizonInInterpCollection(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        if seisColID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format("SEISMIC_COL_0"))
        #Need to check there is a seismic in the collection otherwise no geometry and cannot add the horizon
        seisIDList=GeoDataSync("get3DSeisIDListCol",self.server,seisColID)
        self.assertFalse(seisIDList==None or seisIDList==0,GDSErr(self.server,"Failed to list seismics from collection"))
        if len(seisIDList)==0:
            self.skipTest("Seismic Collection '{}' has no seismics so no horizon can be added".format("SEISMIC_COL_0"))
        interpID=self.repo.getInterpretationCollectionID(INTERP_COL_0)
        if interpID==None:
            self.skipTest("Required Interpretation Collection with asset repository name '{}' not found".format("INTERP_COL_0")) 
        args=[0,seisColID,interpID]
        hzID=self.repo.createHorizon(HORIZON_2,*args)
        self.assertFalse(hzID==None or hzID==0,GDSErr(self.server,"Failed createHorizon in interp collection"))
    
    def testCreate3DHorizonBy3DVolumeInInterpCollection(self):
        seisID=self.repo.get3DSeismicID(SEISMIC3D_0)
        if seisID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format("SEISMIC3D_0")) 
        interpID=self.repo.getInterpretationCollectionID(INTERP_COL_0)
        if interpID==None:
            self.skipTest("Required Interpretation Collection with asset repository name '{}' not found".format("INTERP_COL_0")) 
        args=[0,seisID,interpID]
        hzID=self.repo.createHorizonByVolume(HORIZON_3,*args)
        self.assertFalse(hzID==None or hzID==0,GDSErr(self.server,"Failed createHorizonBy3DVolume in interp collection"))
        
    def testGet3DHorzIDListAndVerify(self):
        hzIDList=GeoDataSync("get3DHorzIDList",self.server)
        self.assertFalse(hzIDList==None or hzIDList==0,GDSErr(self.server,"Failed call to get3DHorzIDList"))
        hz0ID=self.repo.getHorizonID(HORIZON_0)
        hz1ID=self.repo.getHorizonID(HORIZON_1)
        hz2ID=self.repo.getHorizonID(HORIZON_2)
        hz3ID=self.repo.getHorizonID(HORIZON_3)
        self.assertTrue(IDInList(IDComparison,hz0ID,hzIDList),"Failed to find horizon in list")
        self.assertTrue(IDInList(IDComparison,hz1ID,hzIDList),"Failed to find horizon in list")
        if hz2ID != None:
            self.assertTrue(IDInList(IDComparison,hz2ID,hzIDList),"Failed to find horizon in list")
        if hz3ID != None:
            self.assertTrue(IDInList(IDComparison,hz3ID,hzIDList),"Failed to find horizon in list")
    
    def testGet3DHorzGeometry(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        hzGeom=GeoDataSync("get3DHorzGeom",self.server,hzID)
        self.assertFalse(hzGeom==None or hzGeom==0,GDSErr(self.server,"Failed to retrieve horizon geometry"))
        testGeom=self.config.get3DSeismicGeometry(False)
        hzGeom.pop(b'HorzID')
        for k in hzGeom.keys():
            self.assertAlmostEqual(hzGeom[k],testGeom[k],4)
        
    def testPut3DHorzValues(self):
        hzVals=self.config.getHorizonVals()
        success=GeoDataSync("put3DHorzValues",self.server,self.repo.getHorizonID(HORIZON_0),hzVals)
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to put3DHorzValues"))
        
    def testGetSeismicValsFromHorizon(self):
        seisID=self.repo.get3DSeismicID(SEISMIC3D_0)
        hzID=self.repo.getHorizonID(HORIZON_0)
        if seisID==None:
            self.skipTest("Seismic SEISMIC3D_0 not found in repository")
        geom=self.config.get3DSeismicGeometry()
        miline=geom.getMinInline()
        mxline=geom.getMinXline()
        ret=GeoDataSync("getSeismicValsFromHorizon",self.server,hzID,seisID,200,202,400,403)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to getSeismicValsFromHorizon"))
        ret1=GeoDataSync("get3DHorzValsInXl",self.server,hzID,miline,miline+geom.getInlineInc(),mxline,mxline+geom.getXlineInc())
        minz=min(ret1[b'HorzVals'])
        maxz=max(ret1[b'HorzVals'])
        minix=(minz-geom.getMinZ())/geom.getZInc()
        minixf=math.floor(minix)
        maxix=(maxz-geom.getMinZ())/geom.getZInc()
        maxixf=math.floor(maxix)
        minz=geom.getMinZ()+minixf*geom.getZInc()
        maxz=geom.getMinZ()+(maxixf+1)*geom.getZInc()
        gotVals=GeoDataSync("get3DSeisTracesRange",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),miline,miline+geom.getInlineInc(),mxline,mxline+geom.getXlineInc(),minz-geom.getZInc()/4.0,maxz+geom.getZInc()/4.0)
        knownIx=[(hzz-minz)/geom.getZInc() for hzz in ret1[b'HorzVals']]
        knownIxf=[math.floor(hzz) for hzz in knownIx]
        knownIxW=[hzz[1]-hzz[0] for hzz in zip(knownIxf,knownIx)]
        vals=[0,0,0,0]
        for i in range(0,4):
            b=0
            a=gotVals[b'Traces'][knownIxf[i]][i]*(1-knownIxW[i])
            if knownIxW[i]>0:
                b=gotVals[b'Traces'][knownIxf[i]+1][i]*(knownIxW[i])
            vals[i]=a+b
        #print(vals)
        for i in range(0,4):
            self.assertAlmostEqual(vals[i],ret[b'SeismicVals'][i],4,"Different seismic values returned on horizon")
        
    def testGet3DHorzDataRange(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        ret=GeoDataSync("get3DHorzDataRange",self.server,hzID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to get3DHorzDataRange"))
        knownVals=self.config.getHorizonVals()
        knownMin=min(knownVals)
        knownMax=max(knownVals)
        self.assertAlmostEquals(knownMin,ret[b'MinValue'],4,"Mismatch in minimum horizon value")
        self.assertAlmostEquals(knownMax,ret[b'MaxValue'],4,"Mismatch in maximum horizon value")
    
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
        self.assertTrue(compareFloatLists(ret[b'HorzVals'],testVals),"Mismatched horizon values")
        
        
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
        
    def testChange3DHorzColormap(self):
        cmID=self.repo.getColormapID(COLORMAP_0)
        if cmID==None:
            self.skipTest("No Colormap ID avaialbale")
        hzID=self.repo.getHorizonID(HORIZON_0)
        ret=GeoDataSync("change3DHorzColormap",self.server,hzID,cmID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to change3DHorzColormap"))
        
    def testCreate3DHorizonProperty(self):
        hzID=self.repo.getHorizonID(HORIZON_0)
        ret=self.repo.createHorizonProperty(hzID,HORIZON_PROP_0)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to create3DHorzProp"))
        
    def testGet3DHorizonPropertyListAndVerify(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        hzID=self.repo.getHorizonID(HORIZON_0)
        propList=GeoDataSync("get3DHorzPropIDList",self.server,hzID)
        self.assertFalse(propList==None or propList==0,GDSErr(self.server,"Failed call to get3DHorzPropIDList"))
        self.assertTrue(IDInList(IDComparison,hzPropID,propList[b"HorzPropIDList"]),GDSErr(self.server,"Failed to find property ID in property list"))

        
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
        self.assertTrue(compareFloatLists(knownPropVals,propVals[b'PropVals']),"Hz property values do not match")
        
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
        #print("{} {} {} {}".format(loIL,hiIL,loXL,hiXL))
        knownData=self.config.getHorizonPropertyVals()
        testVals=[]
        for ilix in range(int((loIL-geom.getMinInline())/geom.getInlineInc()),int((hiIL-geom.getMinInline())/geom.getInlineInc())+1):
            for xlix in range(int((loXL-geom.getMinXline())/geom.getXlineInc()),int((hiXL-geom.getMinXline())/geom.getXlineInc())+1):
                #print("{} {}".format(ilix,xlix))
                ix=ilix*xlines+xlix
                testVals.append(knownData[int(ix)])
        ret=GeoDataSync("get3DHorzPropValsInXl",self.server,hzPropID,loIL,hiIL,loXL,hiXL)
        self.assertFalse(ret is None or ret==0,GDSErr(self.server,"Failed call to get3DHorzPropValsInXl"))
        #print(testVals)
        #print(ret[b'PropVals'])
        self.assertTrue(compareFloatLists(ret[b'PropVals'],testVals),"Mismatched property values")
        
        
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
      
        
    def testGet3DHorzPropDataRange(self):
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        ret=GeoDataSync("get3DHorzPropDataRange",self.server,hzPropID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to get3DHorzPropDataRange"))
        knownData=self.config.getHorizonPropertyVals()
        knownMin=min(knownData)
        knownMax=max(knownData)
        self.assertAlmostEquals(knownMin,ret[b'MinValue'],4,"Mismatch in minimum horizon property value")
        self.assertAlmostEquals(knownMax,ret[b'MaxValue'],4,"Mismatch in maximum horizon property value")
        
    def testChange3DHorzPropColormap(self):
        cmID=self.repo.getColormapID(COLORMAP_0)
        if cmID==None:
            self.skipTest("No Colormap ID available")
        hzPropID=self.repo.getHorizonPropertyID(HORIZON_PROP_0)
        ret=GeoDataSync("change3DHorzPropColormap",self.server,hzPropID,cmID)
        self.assertFalse(ret==0,GDSErr(self.server,"Failed call to change3DHorzPropColormap"))
        
        
    def testCreate2DHorz(self):
        colID=self.repo.getSeismicCollectionID(SEISMIC_COL_1)
        if colID==None:
            self.skipTest("No 2D Seismic Collection available")
        lineID=self.repo.get2DSeismicID(SEISMIC2D_0)
        if colID==None:
            self.skipTest("No 2D Seismic Line available")
        args=[0,colID,lineID]
        horzID=self.repo.createHorizon2D(HORIZON2D_0,*args)
        self.assertFalse(horzID==None or horzID==0,GDSErr(self.server,"Failed create 2D Horizon"))
	
    def testGet2DHorzListAndVerify(self):
        idList=GeoDataSync("get2DHorzIDList",self.server)
        self.assertFalse(idList==None or idList==0,GDSErr(self.server,"Failed to get2DHorzIDList"))
        hID=self.repo.getHorizon2DID(HORIZON2D_0)
        self.assertTrue(IDInList(hID,idList),"Failed to find 2D horizon in list")
        
    def testPut2DHorzValues(self):
        horzID=self.repo.getHorizon2DID(HORIZON2D_0)
        horzVals=self.config.get2DHorizonVals()
        ret=GeoDataSync("put2DHorzValues",self.server,horzID,horzVals["XCoords"],horzVals["YCoords"],horzVals["Vals"])
        self.assertFalse(horzID==None or ret==0,GDSErr(self.server,"Failed call to put2DHorzValues"))	

    def testGet2DHorzValsAll(self):
        horzID=self.repo.getHorizon2DID(HORIZON2D_0)
        retVals=GeoDataSync("get2DHorzValsAll",horzID)
        horzVals=self.config.get2DHorizonVals()
        self.assertTrue(compareFloatLists(retVals[b'XCoords'],horzVals["XCoords"]),"XCoords did not match in get2DHorzValsAll")
        self.assertTrue(compareFloatLists(retVals[b'YCoords'],horzVals["YCoords"]),"YCoords did not match in get2DHorzValsAll")
        self.assertTrue(compareFloatLists(retVals[b'HorzVals'],horzVals["Vals"]),"Horizon Values did not match in get2DHorzValsAll")
        
		

		
# <!-- FUNCTION get2DHorzValsSpec -->
		# <function name="get2DHorzValsSpec">
			# <signature>
				# <input>
					# <argument internalID="HorzID" type="tnVStr8" />	
					# <argument internalID="LineID" type="tnVStr8" />	
				# </input>
				# <output>
					# <structure>
						# <field internalID="HorzID" type="tnVStr8"/>
						# <field internalID="isDepth" type="tnInt32"/>
						# <field internalID="HorzVals" type="tnVFloat"/>
						# <field internalID="XCoords" type="tnVDouble"/>
						# <field internalID="YCoords" type="tnVDouble"/>	
					# </structure>
				# </output>
			# </signature>
		# </function>	
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizon"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizonBy3DVolume"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizonInInterpCollection"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizonBy3DVolumeInInterpCollection"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzIDListAndVerify"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzGeometry"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzValues"))
        suite.addTest(HorizonTestCase(server,repo,config,"testChange3DHorzColormap"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGetSeismicValsFromHorizon"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzDataRange")) 
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzVals"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzValsInXl"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzValuesSpec"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate3DHorizonProperty"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorizonPropertyListAndVerify"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzPropValues"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzPropDataRange"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzPropVals"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet3DHorzPropValsInXl"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut3DHorzPropValuesSpec"))
        suite.addTest(HorizonTestCase(server,repo,config,"testChange3DHorzPropColormap"))
        suite.addTest(HorizonTestCase(server,repo,config,"testCreate2DHorz"))
        suite.addTest(HorizonTestCase(server,repo,config,"testGet2DHorzListAndVerify"))
        suite.addTest(HorizonTestCase(server,repo,config,"testPut2DHorzValues"))
        #suite.addTest(HorizonTestCase(server,repo,config,"testGet2DHorzValsAll"))
        
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
    return HorizonTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
            
    
    
    