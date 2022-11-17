# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:52:26 2022

This module is for test functions concerned 
with 'get3DSeisTracesTransect' and is intended mainly for help in development
and debugging

@author: lewthwju
"""
import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest
from executor import TestExecutor


from test_utils import compareFloatLists    
from test_utils import makeCreationGeometryFromFullGeometry 
from test_utils import IDInList
from test_utils import GDSErr 
from test_utils import getNearestIntegerInRange
from test_utils import getNearestIntegerLessThanInRange
from test_utils import bilinearTraceInterp


from constants import SEISMIC_COL_0
from constants import SEISMIC_COL_1
from constants import SEISMIC_COL_3
from constants import SEISMIC3D_0
from constants import SEISMIC3D_2
from constants import SEISMIC2D_0

GeoDataSync=None
IDComparison=None

__unittest=True

TestTransGeometry={
        b'MinInline': 200,
        b'MaxInline': 220,
        b'InlineInc': 2,
        b'MinXline': 300,
        b'MaxXline': 330,
        b'XlineInc': 3,
        b'X0': 100.0,
        b'Y0': 100.0,
        b'X1': 200.0,
        b'Y1': 200.0,
        b'X2': 200.0,
        b'Y2': 100.0,
        b'MinZ': 0.0,
        b'MaxZ': 0.1,
        b'ZInc': 0.005,
        b'InlineSep': 10.0,
        b'XlineSep': 10.0,
        b'isDepth': 0
        }

class TransectTestCase(unittest.TestCase):

    def __init__(self,server,repo,config,methodName):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
   
    
    def testCreateSeismicCollection(self):
        seisColID=self.repo.createSeismicCollection(SEISMIC_COL_0)
        self.assertFalse(seisColID is None or seisColID==0,GDSErr(self.server,"Failed to create Seismic Collection:"))
    
   
          
    def testCreate3DSeismic(self):
        args=[self.repo.getSeismicCollectionID(SEISMIC_COL_0)]
        geom=makeCreationGeometryFromFullGeometry(self.config.get3DSeismicGeometry(False))
        args.extend(list(geom.values()))
        seisID=self.repo.create3DSeismic(SEISMIC3D_0,*args);
        self.assertFalse(seisID is None or seisID==0,GDSErr(self.server,"Failed create3DSeismic"))
        
        
   
        
    '''
    Put the fidicual data into the cube
    '''
    def testPut3DSeisTraces(self):
         geom=self.config.get3DSeismicGeometry(False)
         ilines,xlines=geom.get3DGeometryILXLPairs()
         samps=round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1
         volumeData=self.config.get3DSeismicData()
         success=GeoDataSync("put3DSeisTraces",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),volumeData,ilines,xlines,len(ilines),samps,geom[b"MinZ"])
         self.assertTrue(success,GDSErr(self.server,"Failed GDS call put3DSeisTrace"))
         
    
     
    
    #@unittest.skip("Test not run due to known errors")
    def testGet3DSeisTracesTransect(self):
        geom=self.config.get3DSeismicGeometry()
        seisID = self.repo.get3DSeismicID(SEISMIC3D_0)
        xinc=(geom[b'X1']-geom[b'X0'])/11.0#10.0
        yinc=(geom[b'Y1']-geom[b'Y0'])/11.0#10.0
        x0 = geom[b'X0']+xinc*3
        y0 = geom[b'Y0']+yinc*6
        x1 = geom[b'X0']+xinc*8
        y1 = geom[b'Y0']+yinc*2
        
        
        minZ = geom[b'MinZ']
        maxZ = geom[b'MinZ']+geom[b'ZInc'] #geom[b'MaxZ']
        #print("MinZ:",minZ,"MaxZ",maxZ)
        numTraces = 5
        dy=(y1-y0)/(numTraces-1)
        dx=(x1-x0)/(numTraces-1)
        ilxls=[]
        xcoords=[]
        ycoords=[]
        for i in range(0,numTraces):
            xcoords.append(x0+i*dx)
            ycoords.append(y0+i*dy)
            ilxl=geom.transformUTM([x0+i*dx,y0+i*dy])
            if geom.gridPtInCube(ilxl[0],ilxl[1]):
                ilxls.append(ilxl)
        for ilxl in ilxls:
            xy=geom.transformILXL([ilxl[0],ilxl[1]])
            #print("ILXL:",ilxl,"XY",xy)
        ilrange=geom.getInlineRange();
        xlrange=geom.getCrosslineRange();
        interpTraces=[]
        for ilxl in ilxls:
            sil=getNearestIntegerLessThanInRange(ilrange,ilxl[0])
            sxl=getNearestIntegerLessThanInRange(xlrange,ilxl[1])
            lil=sil+geom.getInlineInc()
            lxl=sxl+geom.getXlineInc()
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,sil,lil,sxl,lxl,minZ,maxZ)
            distIL=(ilxl[0]-sil)/geom.getInlineInc();
            distXL=(ilxl[1]-sxl)/geom.getXlineInc();
            #print("distIL:",distIL,"distXL",distXL)
            #print(traces[b'Traces'])
            #print(traces)
            interpTrace=bilinearTraceInterp(distIL,distXL,traces[b'Traces'])
            interpTraces.append(interpTrace)
        #print(interpTraces)
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        #print(reshapedInterps)
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        reshapedLen=len(reshapedInterps)
        #print(reshapedLen)
        #print(seisTransect)
        self.assertFalse(nTraces==None or nTraces==0,GDSErr(self.server,"Incorrect no. of Traces from get3DSeisTracesTransect"))
        self.assertFalse(tracesLength==None or tracesLength==0,GDSErr(self.server,"Incorrect Traces length from get3DSeisTracesTransect"))
        for i in range(0,reshapedLen):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],reshapedInterps[i]),"get3DSeisTracesTransect data values do not match")
                
    def testGet3DSeisTracesTransectCorners(self):
        geom=self.config.get3DSeismicGeometry()
        seisID = self.repo.get3DSeismicID(SEISMIC3D_0)
        x0 = geom[b'X0']
        y0 = geom[b'Y0']
        x1=geom[b'X1']
        y1=(geom[b'Y1'])
        minZ = geom[b'MinZ']
        maxZ = geom[b'MinZ']+geom[b'ZInc'] #geom[b'MaxZ']
        numTraces = 2
        #print(x0,x1,y0,y1,minZ,maxZ)
        ilxls=[geom.transformUTM([x0,y0]),geom.transformUTM([x1,y1])]
        interpTraces=[[],[]]
        for ilxl in ilxls:
            nil=round(ilxl[0])
            nxl=round(ilxl[1])
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,nil,nil,nxl,nxl,minZ,maxZ)
            for i in range(2):
                interpTraces[i].append(traces[b'Traces'][i][0])
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        #print(seisTransect)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        self.assertTrue(nTraces==numTraces,"Incorrect no. of Traces from get3DSeisTracesTransect")
        self.assertTrue(tracesLength==2 ,"Incorrect Traces length from get3DSeisTracesTransect")
        for i in range(0,tracesLength):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],interpTraces[i]),"get3DSeisTracesTransect data values do not match")
                
    def testGet3DSeisTracesTransectCloseToLine(self):
        geom=self.config.get3DSeismicGeometry()
        seisID = self.repo.get3DSeismicID(SEISMIC3D_0)
        x0 = geom[b'X0']
        y0 = geom[b'Y0']
        x1=geom[b'X1']
        y1=(geom[b'Y1'])
        minZ = geom[b'MinZ']
        maxZ = geom[b'MinZ']+geom[b'ZInc'] #geom[b'MaxZ']
       
       
        minIL=geom.getMinInline()
        minXL=geom.getMinXline()
        maxXL=geom.getMaxXline()
        numTraces=(maxXL-minXL)/geom.getXlineInc()+3
        #print(numTraces)
        ilxls=[]
        
        for i in range(0,int(numTraces)):
            ilxls.append([minIL+geom.getInlineInc()*1.1,minXL-geom.getXlineInc()*0.9+(geom.getXlineInc())*(i+3)])
        [x0,y0]=geom.transformILXL(ilxls[0])
        [x1,y1]=geom.transformILXL(ilxls[len(ilxls)-1])
        interpTraces=[]
        ilrange=geom.getInlineRange();
        xlrange=geom.getCrosslineRange();
        for ilxl in ilxls:
            sil=getNearestIntegerLessThanInRange(ilrange,ilxl[0])
            sxl=getNearestIntegerLessThanInRange(xlrange,ilxl[1])
            lil=sil+geom.getInlineInc()
            lxl=sxl+geom.getXlineInc()
            #print(ilxl[0],ilxl[1],sil,sxl)
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,sil,lil,sxl,lxl,minZ,maxZ)
            if not traces==0:
                 distIL=(ilxl[0]-sil)/geom.getInlineInc();
                 distXL=(ilxl[1]-sxl)/geom.getXlineInc();
                 #print("il",ilxl[0],"xl",ilxl[1],"distIL:",distIL,"distXL",distXL)
                 #print(traces[b'Traces'])
                 # print(traces)
                 interpTrace=bilinearTraceInterp(distIL,distXL,traces[b'Traces'])
                 interpTraces.append(interpTrace)
               
        #print(interpTraces)
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        #print(reshapedInterps)
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, int(numTraces))
        #print(seisTransect)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        self.assertFalse(nTraces==None or nTraces==0,GDSErr(self.server,"Incorrect no. of Traces from get3DSeisTracesTransect"))
        self.assertFalse(tracesLength==None or tracesLength==0,GDSErr(self.server,"Incorrect Traces length from get3DSeisTracesTransect"))
        for i in range(0,tracesLength):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],reshapedInterps[i]),"get3DSeisTracesTransect data values do not match")
        
    
    # The following tests relate to a simple cube with the following geome
    def testCreateSeismicCollectionForTransect(self):
        seisColID=self.repo.createSeismicCollection(SEISMIC_COL_3)
        self.assertFalse(seisColID is None or seisColID==0,GDSErr(self.server,"Failed to create Seismic Collection:"))
    
    def testCreate3DSeismicForTransect(self):
        args = [self.repo.getSeismicCollectionID(SEISMIC_COL_3)]
        geom = makeCreationGeometryFromFullGeometry(TestTransGeometry)
        args.extend(list(geom.values()))
        seisID=self.repo.create3DSeismic(SEISMIC3D_2,*args);
        self.assertFalse(seisID is None or seisID==0, GDSErr(self.server,"Failed to create volume for transect"))
 
    def testPut3DSeisTracesForTransect(self):
        minZ = TestTransGeometry[b'MinZ']
        maxZ = TestTransGeometry[b'MaxZ']
        ZInc = TestTransGeometry[b'ZInc']
        gotData=GeoDataSync("get3DSeisTracesAll",self.server,self.repo.get3DSeismicID(SEISMIC3D_2),minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesAll"))
        returnedTraces=gotData[b'Traces']
        nTraces = len(returnedTraces[0])
        traceLen = len(returnedTraces)
        for i in range(nTraces):
            for j in range(traceLen):
                returnedTraces[j][i] = i+1 + j*ZInc;
        # Now need to put back in volume.
        success = GeoDataSync("put3DSeisTraces", self.server,self.repo.get3DSeismicID(SEISMIC3D_2),returnedTraces, gotData[b'Inlines'], gotData[b'Xlines'],gotData[b'NumTraces'],gotData[b'TraceLength'],gotData[b'Z0'])
        self.assertTrue(success,GDSErr(self.server,"Failed GDS call put3DSeisTraces for transect"))
        
    def compareTransect(self,transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0):
        #print(" NumTraces: ",transect[b'NumTraces'])
        self.assertTrue(transect[b'NumTraces'] == Expected_NumTraces, GDSErr(self.server,"Wrong number of traces returned"))
        
        #print("Tracelength: ",transect[b'TraceLength'])
        self.assertTrue(transect[b'TraceLength'] == Expected_TraceLength, GDSErr(self.server,"Wrong trace length returned"))
        
        #print("Z0: ",transect[b'Z0'])
        self.assertTrue(transect[b'Z0'] == Expected_Z0, GDSErr(self.server,"Wrong Z0 value returned"))
        
        #print("ZInc: ",transect[b'ZInc'])
        self.assertTrue(transect[b'ZInc'] == Expected_ZInc, GDSErr(self.server,"Wrong ZInc value returned"))
    
        # Check that know 'good' values are returned for traces   
        ans = compareFloatLists(Expected_XCoords, transect[b'XCoords'])
        self.assertTrue(ans==True, GDSErr(self.server,"Incorrect Xlines returned"))

        ans = compareFloatLists(Expected_YCoords, transect[b'YCoords'])
        self.assertTrue(ans==True, GDSErr(self.server,"Incorrect Ylines returned"))
        
        ans = compareFloatLists(Expected_dists, transect[b'Distance'])
        self.assertTrue(ans==True, GDSErr(self.server,"Incorrect distance returned"))
        
        returnedTops = transect[b'Traces'][0]
        ans = compareFloatLists(Expected_vals0, returnedTops)
        self.assertTrue(ans==True, GDSErr(self.server,"Incorrect Traces returned"))

        return

    def testBottomComplete(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 100.0
        Y1 = 100.0
        X2 = 120.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0]
        Expected_YCoords = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        Expected_dists = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        Expected_vals0 = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3.0]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)
        
    def testAboveBottomComplete(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 100.0
        Y1 = 105.0
        X2 = 120.0
        Y2 = 105.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0]
        Expected_YCoords = [105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0]
        Expected_dists = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        Expected_vals0 = [6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testBottomFromBefore(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 90.0
        Y1 = 100.0
        X2 = 120.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 7
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [102.0, 105.0, 108.0, 111.0, 114.0, 117.0, 120.0]
        Expected_YCoords = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        Expected_dists = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
        Expected_vals0 = [1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testBottomFromBeforeShorter(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 90.0
        Y1 = 100.0
        X2 = 110.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 6
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0]
        Expected_YCoords = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        Expected_dists = [2.0, 2.0, 2.0, 2.0, 2.0]
        Expected_vals0 = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testBottomFromBeforeOverlapEachEnd(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 50.0
        Y1 = 100.0
        X2 = 250.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 5
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [110.0, 130.0, 150.0, 170.0, 190.0]
        Expected_YCoords = [100.0, 100.0, 100.0, 100.0, 100.0]
        Expected_dists = [20, 20, 20, 20]
        Expected_vals0 = [2.0, 4.0, 6.0, 8.0, 10]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testBottomOneTraceReturned(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 90.0
        Y1 = 100.0
        X2 = 100.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 1
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [100.0]
        Expected_YCoords = [100.0]
        Expected_dists = [0]
        Expected_vals0 = [1]
        # Test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testDiagonalOverlap(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 90.0
        Y1 = 120.0
        X2 = 120.0
        Y2 = 90.0
        # Expected returns
        Expected_NumTraces = 3
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [102.0, 105.0, 108.0]
        Expected_YCoords = [108.0, 105.0, 102.0]
        Expected_dists = [4.2426, 4.2426]
        Expected_vals0 = [10.0, 7.0, 4.0]
        # Do the test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testDiagonalTouchBothEdges(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 100.0
        Y1 = 130.0
        X2 = 120.0
        Y2 = 100.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0]
        Expected_YCoords = [130.0, 127.0, 124.0, 121.0, 118.0, 115.0, 112.0, 109.0, 106.0, 103.0, 100.0]
        Expected_dists = [3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056]
        Expected_vals0 = [34.0, 30.9, 27.8, 24.7, 21.6, 18.5, 15.4, 12.3, 9.2, 6.10, 3] 
        # Do test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testDiagonalInside(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 110.0
        Y1 = 140.0
        X2 = 130.0
        Y2 = 110.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [110.0, 112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0, 126.0, 128.0, 130.0]
        Expected_YCoords = [140.0, 137.0, 134.0, 131.0, 128.0, 125.0, 122.0, 119.0, 116.0, 113.0, 110.0]
        Expected_dists = [3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056]
        Expected_vals0 = [46.0, 42.9, 39.8, 36.7, 33.6, 30.5, 27.4, 24.3, 21.2, 18.1, 15.0] 
        # Do test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testDiagonalInside(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 110.0
        Y1 = 140.0
        X2 = 130.0
        Y2 = 110.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [110.0, 112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0, 126.0, 128.0, 130.0]
        Expected_YCoords = [140.0, 137.0, 134.0, 131.0, 128.0, 125.0, 122.0, 119.0, 116.0, 113.0, 110.0]
        Expected_dists = [3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056, 3.6056]
        Expected_vals0 = [46.0, 42.9, 39.8, 36.7, 33.6, 30.5, 27.4, 24.3, 21.2, 18.1, 15.0] 
        # Do test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        

    def testWhollyOutside(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 10.0
        Y1 = 40.0
        X2 = 30.0
        Y2 = 10.0
        # Expected return: "No traces returned on the transect."
        # Do test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect,GDSErr(self.server,"Succeeded GDS call but with invalid transect"))
        errMsg=GeoDataSync("getLastError",self.server)
        self.assertTrue(errMsg==b'No traces returned on the transect.')

    def testVerySmall(self):
        seisID = self.repo.get3DSeismicID(SEISMIC3D_2)
        # inputs
        X1 = 105.0
        Y1 = 105.0
        X2 = 106.0
        Y2 = 105.0
        # Expected returns
        Expected_NumTraces = 11
        Expected_TraceLength = 21
        Expected_Z0 = 0.0
        Expected_ZInc = 0.005
        Expected_XCoords = [105.0, 105.1, 105.2, 105.3, 105.4, 105.5, 105.6, 105.7, 105.8, 105.9, 106.0]
        Expected_YCoords = [105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0, 105.0]
        Expected_dists = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        Expected_vals0 = [7.00, 7.01, 7.02, 7.03, 7.04, 7.05, 7.06, 7.07, 7.08, 7.09, 7.10] 
        # Do test
        transect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, X1, Y1, X2, Y2, 0.0, 0.1, 11)
        self.assertFalse(transect==None or transect ==0, GDSErr(self.server, "Failed to get transect"))
        self.compareTransect(transect, Expected_NumTraces, Expected_TraceLength, Expected_Z0 ,Expected_ZInc,Expected_XCoords,Expected_YCoords,Expected_dists,Expected_vals0)        
		
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
       suite.addTest(TransectTestCase(server,repo,config,"testCreateSeismicCollection"))
       suite.addTest(TransectTestCase(server,repo,config,"testCreate3DSeismic"))
       suite.addTest(TransectTestCase(server,repo,config,"testPut3DSeisTraces"))
       
       suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransect"))
       suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransectCorners"))
       suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransectCloseToLine"))
       
	   # Additional transect tests using a known small volume
       suite.addTest(TransectTestCase(server,repo,config,"testCreateSeismicCollectionForTransect"))
       suite.addTest(TransectTestCase(server,repo,config,"testCreate3DSeismicForTransect"))
       suite.addTest(TransectTestCase(server,repo,config,"testPut3DSeisTracesForTransect"))
       #Transects along an edge
       suite.addTest(TransectTestCase(server,repo,config, "testBottomComplete"))
       suite.addTest(TransectTestCase(server,repo,config, "testAboveBottomComplete"))
       suite.addTest(TransectTestCase(server,repo,config, "testBottomFromBefore"))
       suite.addTest(TransectTestCase(server,repo,config, "testBottomFromBeforeShorter"))
       suite.addTest(TransectTestCase(server,repo,config, "testBottomFromBeforeOverlapEachEnd"))
       suite.addTest(TransectTestCase(server,repo,config, "testBottomOneTraceReturned"))
       #Transects along a diagonal
       suite.addTest(TransectTestCase(server,repo,config, "testDiagonalOverlap"))
       suite.addTest(TransectTestCase(server,repo,config, "testDiagonalTouchBothEdges"))
       suite.addTest(TransectTestCase(server,repo,config, "testDiagonalInside"))
       suite.addTest(TransectTestCase(server,repo,config, "testWhollyOutside"))
       #Very small transect
       suite.addTest(TransectTestCase(server,repo,config,"testVerySmall"))
	   
              
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
    return TransectTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
   
   