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
from constants import SEISMIC3D_0
from constants import SEISMIC2D_0

GeoDataSync=None
IDComparison=None

__unittest=True


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
        print("MinZ:",minZ,"MaxZ",maxZ)
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
            print("ILXL:",ilxl,"XY",xy)
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
            print("distIL:",distIL,"distXL",distXL)
            print(traces[b'Traces'])
            print(traces)
            interpTrace=bilinearTraceInterp(distIL,distXL,traces[b'Traces'])
            interpTraces.append(interpTrace)
        #print(interpTraces)
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        print(reshapedInterps)
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        reshapedLen=len(reshapedInterps)
        print(reshapedLen)
        print(seisTransect)
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
        print(x0,x1,y0,y1,minZ,maxZ)
        ilxls=[geom.transformUTM([x0,y0]),geom.transformUTM([x1,y1])]
        interpTraces=[]
        for ilxl in ilxls:
            nil=round(ilxl[0])
            nxl=round(ilxl[1])
            #print(ilxl[0],ilxl[1],nil,nxl)
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,nil,nil,nxl,nxl,minZ,maxZ)
            interpTraces.append(traces[b'Traces'])
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        self.assertFalse(nTraces==None or nTraces==0,GDSErr(self.server,"Incorrect no. of Traces from get3DSeisTracesTransect"))
        self.assertFalse(tracesLength==None or tracesLength==0,GDSErr(self.server,"Incorrect Traces length from get3DSeisTracesTransect"))
        for i in range(0,tracesLength):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],reshapedInterps[i]),"get3DSeisTracesTransect data values do not match")
                
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
        print(numTraces)
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
            print(ilxl[0],ilxl[1],sil,sxl)
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,sil,lil,sxl,lxl,minZ,maxZ)
            if not traces==0:
                 distIL=(ilxl[0]-sil)/geom.getInlineInc();
                 distXL=(ilxl[1]-sxl)/geom.getXlineInc();
                 
                 print("il",ilxl[0],"xl",ilxl[1],"distIL:",distIL,"distXL",distXL)
                 print(traces[b'Traces'])
                # print(traces)
                 interpTrace=bilinearTraceInterp(distIL,distXL,traces[b'Traces'])
                 interpTraces.append(interpTrace)
               
        print(interpTraces)
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        print(reshapedInterps)
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        print(seisTransect)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        self.assertFalse(nTraces==None or nTraces==0,GDSErr(self.server,"Incorrect no. of Traces from get3DSeisTracesTransect"))
        self.assertFalse(tracesLength==None or tracesLength==0,GDSErr(self.server,"Incorrect Traces length from get3DSeisTracesTransect"))
        for i in range(0,tracesLength):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],reshapedInterps[i]),"get3DSeisTracesTransect data values do not match")
        
    
   
        
        
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
       suite.addTest(TransectTestCase(server,repo,config,"testCreateSeismicCollection"))
       suite.addTest(TransectTestCase(server,repo,config,"testCreate3DSeismic"))
       suite.addTest(TransectTestCase(server,repo,config,"testPut3DSeisTraces"))
       
       #suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransect"))
       #suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransectCorners"))
       suite.addTest(TransectTestCase(server,repo,config,"testGet3DSeisTracesTransectCloseToLine"))
       
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
   
   