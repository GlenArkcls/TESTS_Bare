# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 14:25:25 2022


Confiogurations Let [t0,t1] be the trace interval (t0<t1)
Then for a query interval [z0,z1] is of type: (z0<z1)
    
0 z0,z1<t0
1 z0<t0,z1=t0
2 z0<t0,t0<z1<t1
3 z0=t0,t0<z1<t1
4 z0=t0,z1=t1
5 t0<z0<t1,t0<z1<t1
6 t0<z0<t1,z1=t1
7 t0<z0<t1,z1>t1
8 z0=t1,z1>t1
9 z0,z1>t1

@author: lewthwju
"""

import os
import sys
import math


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest
from executor import TestExecutor
from seismicgeometry import SeismicGeometry


from test_utils import compareFloatLists    
from test_utils import makeCreationGeometryFromFullGeometry 
from test_utils import IDInList
from test_utils import GDSErr 
from test_utils import getNearestIntegerInRange
from test_utils import bilinearTraceInterp


from constants import SEISMIC_COL_0
from constants import SEISMIC_COL_1
from constants import SEISMIC3D_0
from constants import SEISMIC2D_0

SEISMIC_ZBOUNDS_COL_0=b"SeismicZBoundsCollection0"
SEISMIC_ZBOUNDS_COL_1=b"SeismicZBoundsCollection1"
SEISMIC_ZBOUNDS_COL_2=b"SeismicZBoundsCollection2"
SEISMIC_ZBOUNDS_COL_3=b"SeismicZBoundsCollection3"

SEISMIC3D_ZBOUNDS_0=b"SeismicZBounds0"
SEISMIC3D_ZBOUNDS_1=b"SeismicZBounds1"
SEISMIC3D_ZBOUNDS_2=b"SeismicZBounds2"
SEISMIC3D_ZBOUNDS_3=b"SeismicZBounds3"

GeoDataSync=None
IDComparison=None

__unittest=True

SeisGeometry={
        b'MinInline': 200,
        b'MaxInline': 201,
        b'InlineInc': 1,
        b'MinXline': 400,
        b'MaxXline': 401,
        b'XlineInc': 1,
        b'X0': 608000.0,
        b'Y0': 6076000.0,
#        b'X1': 608000.0,
#        b'Y1': 6076000.0,
#        b'X2': 608000.0,
#        b'Y2': 6076000.0,
        b'X1': 608025.0,
        b'Y1': 6076025.0,
        b'X2': 608000.0,
        b'Y2': 6076025.0,
        b'MinZ': 0.0,
        b'MaxZ': 4.0,
        b'ZInc': 0.002,
        b'InlineSep': 25.0,
        b'XlineSep': 25.0,
        b'isDepth': 0
        }


class SeismicZBoundsQueryTestCase(unittest.TestCase):
    
    def __init__(self,server,repo,config,methodName,seisCol):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
        self.seisCol=seisCol
     
    def createSeismic(self):
        sid=SEISMIC3D_ZBOUNDS_0
        colid=SEISMIC_ZBOUNDS_COL_0
        
        
        if self.seisCol==0:
            SeisGeometry[b'MinZ']=0.0
            SeisGeometry[b'ZInc']=0.002
            SeisGeometry[b'MaxZ']=4.0
        elif self.seisCol==1:
            SeisGeometry[b'MinZ']=-0.4
            SeisGeometry[b'ZInc']=0.001
            SeisGeometry[b'MaxZ']=3.0
            sid=SEISMIC3D_ZBOUNDS_1
            colid=SEISMIC_ZBOUNDS_COL_1
        elif self.seisCol==2:
            SeisGeometry[b'MinZ']=-0.452
            SeisGeometry[b'ZInc']=0.004
            SeisGeometry[b'MaxZ']=4.0
            sid=SEISMIC3D_ZBOUNDS_2
            colid=SEISMIC_ZBOUNDS_COL_2
        elif self.seisCol==3:
            SeisGeometry[b'MinZ']=-2.44
            SeisGeometry[b'ZInc']=0.002
            SeisGeometry[b'MaxZ']=6.0
            sid=SEISMIC3D_ZBOUNDS_3
            colid=SEISMIC_ZBOUNDS_COL_3
        args=[self.repo.getSeismicCollectionID(colid)]
        geom=makeCreationGeometryFromFullGeometry(SeisGeometry)
        args.extend(list(geom.values()))
        seisID=self.repo.create3DSeismic(sid,*args)
        self.assertFalse(seisID==0,GDSErr(self.server,"Failed to create the seismic"))
        #Put the data
        samps=round((geom[b'MaxZ']-geom[b'MinZ'])/geom[b'ZInc'])+1
        data=[[float(i)]*4 for i in range(0,samps)]
        geometry=SeismicGeometry(geom)
        ilines,xlines=geometry.get3DGeometryILXLPairs()
        success=GeoDataSync("put3DSeisTraces",self.server,self.repo.get3DSeismicID(sid),data,ilines,xlines,len(ilines),samps,geom[b"MinZ"])
        self.assertFalse(success==0,GDSErr(self.server,"Failed to put trace data into seismic"))
    
    def createSeismicCollection(self):
        colID=SEISMIC_ZBOUNDS_COL_0
        if self.seisCol==1:
            colID=SEISMIC_ZBOUNDS_COL_1
        elif self.seisCol==2:
            colID=SEISMIC_ZBOUNDS_COL_2
        elif self.seisCol==3:
            colID=SEISMIC_ZBOUNDS_COL_3
                
        seisColID=self.repo.createSeismicCollection(colID)
        self.assertFalse(seisColID is None or seisColID==0,GDSErr(self.server,"Failed to create Seismic ZBounds Collection:"))
       
    def getSampleNo(self,z):
        '''Returns sample number as a float (ie may be in between samples)
        '''
        sn=(z-SeisGeometry[b'MinZ'])/SeisGeometry[b'ZInc']
        return round(sn)
    
    def executeQueries(self,z0,z1):
        #print("XCUTE",z0,z1)
        
        minIL=200
        minXL=400
        maxIL=200
        maxXL=400
        ilines=[200]
        xlines=[400]
        ilLineNo=200
        xlLineNo=400
        if self.seisCol==0:
          sid=SEISMIC3D_ZBOUNDS_0
        elif self.seisCol==1:
          sid=SEISMIC3D_ZBOUNDS_1
        elif self.seisCol==2:
          sid=SEISMIC3D_ZBOUNDS_2
        elif self.seisCol==3:
          sid=SEISMIC3D_ZBOUNDS_3
            
        seisID=self.repo.get3DSeismicID(sid)
        allRet=GeoDataSync("get3DSeisTracesAll",self.server,seisID,z0,z1)
        #self.assertFalse(allRet is None or allRet==0,GDSErr(self.server,"get3DSeisTracesAll in executeQueries"))
        rangeRet=GeoDataSync("get3DSeisTracesRange",self.server,seisID,minIL,maxIL,minXL,maxXL,z0,z1)
        #self.assertFalse(rangeRet is None or rangeRet==0,GDSErr(self.server,"get3DSeisTracesRange in executeQueries"))
        inXIilRet=GeoDataSync("get3DSeisTracesInXl",self.server,seisID,1,ilLineNo,z0,z1)
        #self.assertFalse(inXIilRet is None or inXIilRet==0,GDSErr(self.server,"get3DSeisTracesInXI (il) in executeQueries"))
        inXIxlRet=GeoDataSync("get3DSeisTracesInXl",self.server,seisID,0,xlLineNo,z0,z1)
        #self.assertFalse(inXIxlRet is None or inXIxlRet==0,GDSErr(self.server,"get3DSeisTracesInXI (xl) in executeQueries"))
        specRet=GeoDataSync("get3DSeisTracesSpec",self.server,seisID,ilines,xlines,z0,z1)
        #self.assertFalse(specRet is None or specRet==0,GDSErr(self.server,"get3DSeisTracesSpec in executeQueries"))
        return [allRet,rangeRet,inXIilRet,inXIxlRet,specRet]
    
    def checkReturns0(self,z0,z1,returns):
        self.assertTrue(len(returns[0][b'Traces'])==0,"Trace length not zero for type 0 All")
        self.assertTrue(returns[1]==0,"Not a zero return for type 0 Range")
        self.assertTrue(len(returns[2][b'Traces'])==0,"Trace length not zero for type 0 InXIil")
        self.assertTrue(len(returns[3][b'Traces'])==0,"Trace length not zero for type 0 InXIxl")
        self.assertTrue(len(returns[4][b'Traces'])==0,"Trace length not zero for type 0 Spec")
        
    def checkReturns1(self,z0,z1,returns):
        self.assertTrue(len(returns[0][b'Traces'])==1,"Trace length not 1 for type 1 All")
        self.assertTrue(len(returns[1][b'Traces'])==1,"Trace length not 1 for type 1 Range")
        self.assertTrue(len(returns[2][b'Traces'])==1,"Trace length not 1 for type 1 InXIil")
        self.assertTrue(len(returns[3][b'Traces'])==1,"Trace length not 1 for type 1 InXIxl")
        self.assertTrue(len(returns[4][b'Traces'])==1,"Trace length not 1 for type 1 Spec")
        self.assertTrue(returns[0][b'Traces'][0][0]==0,"Wrong trace value type 1 All")
        self.assertTrue(returns[1][b'Traces'][0][0]==0,"Wrong trace value type 1 Range")
        self.assertTrue(returns[2][b'Traces'][0][0]==0,"Wrong trace value type 1 InXIil")
        self.assertTrue(returns[3][b'Traces'][0][0]==0,"Wrong trace value type 1 InXIxl")
        self.assertTrue(returns[4][b'Traces'][0][0]==0,"Wrong trace value type 1 Spec")
        
    def checkReturns2(self,z0,z1,returns):
        z0=SeisGeometry[b'MinZ']
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 2 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 2 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 2 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 2 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 2 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 2 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 2 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 2 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 2 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 2 Spec");
        
    def checkReturns3(self,z0,z1,returns):
        z0=SeisGeometry[b'MinZ']
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        print("No of samps=",samps)
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 3 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 3 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 3 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 3 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 3 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 3 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 3 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 3 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 3 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 3 Spec");
        
    def checkReturns4(self,z0,z1,returns):
        z0=SeisGeometry[b'MinZ']
        z1=SeisGeometry[b'MaxZ']
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        print("No of samps=",samps)
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 4 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 4 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 4 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 4 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 4 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 4 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 4 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 4 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 4 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 4 Spec");
        
    def checkReturns5(self,z0,z1,returns):
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        print("No of samps=",samps)
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 5 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 5 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 5 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 5 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 5 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 5 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 5 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 5 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 5 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 5 Spec");
        
    def checkReturns6(self,z0,z1,returns):
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        print("No of samps=",samps)
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 6 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 6 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 6 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 6 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 6 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 6 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 6 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 6 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 6 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 6 Spec");
        
    def checkReturns7(self,z0,z1,returns):
        z1=SeisGeometry[b'MaxZ']
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        print("No of samps=",samps)
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 7 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 7 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 7 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 7 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 7 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 7 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 7 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 7 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 7 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 7 Spec");
        
    def checkReturns8(self,z0,z1,returns):
        z0=SeisGeometry[b'MaxZ']
        z1=SeisGeometry[b'MaxZ']
        s0=self.getSampleNo(z0)
        s1=self.getSampleNo(z1)
        cs0=math.ceil(s0)
        fs1=math.floor(s1)
        samps=fs1-cs0+1
        self.assertTrue(returns[0][b'TraceLength']==samps,"Trace length incorrect for type 7 All")
        self.assertTrue(returns[1][b'TraceLength']==samps,"Trace length incorrect for type 7 Range")
        self.assertTrue(returns[2][b'TraceLength']==samps,"Trace length incorrect for type 7 InXIil")
        self.assertTrue(returns[3][b'TraceLength']==samps,"Trace length incorrect for type 7 InXIxl")
        self.assertTrue(returns[4][b'TraceLength']==samps,"Trace length incorrect for type 7 Spec")
        data=[float(i) for i in range(cs0,fs1+1)]
        data0=[returns[0][b'Traces'][i][0] for i in range(0,samps)]
        data1=[returns[1][b'Traces'][i][0] for i in range(0,samps)]
        data2=[returns[2][b'Traces'][i][0] for i in range(0,samps)]
        data3=[returns[3][b'Traces'][i][0] for i in range(0,samps)]
        data4=[returns[4][b'Traces'][i][0] for i in range(0,samps)]
        self.assertTrue(compareFloatLists(data,data0),"Wrong data returned for type 7 All");
        self.assertTrue(compareFloatLists(data,data1),"Wrong data returned for type 7 Range");
        self.assertTrue(compareFloatLists(data,data2),"Wrong data returned for type 7 InXIil");
        self.assertTrue(compareFloatLists(data,data3),"Wrong data returned for type 7 InXIxl");
        self.assertTrue(compareFloatLists(data,data4),"Wrong data returned for type 7 Spec");
        
    def checkReturns9(self,z0,z1,returns):
        self.assertTrue(len(returns[0][b'Traces'])==0,"Trace length not zero for type 0 All")
        self.assertTrue(returns[1]==0,"Not a zero return for type 0 Range")
        self.assertTrue(len(returns[2][b'Traces'])==0,"Trace length not zero for type 0 InXIil")
        self.assertTrue(len(returns[3][b'Traces'])==0,"Trace length not zero for type 0 InXIxl")
        self.assertTrue(len(returns[4][b'Traces'])==0,"Trace length not zero for type 0 Spec")
    
    def checkRollingReturns(self,z0,z1,returns):
        failed0=returns[0][b'TraceLength']!=2
        if failed0:
            print("Failed 0",z0,z1,returns[0][b'TraceLength'],returns[0][b'Z0'])
        else:
            print("Passed 0",z0,z1,returns[0][b'TraceLength'],returns[0][b'Z0'])
        failed1=returns[1]==0 or returns[1][b'TraceLength']!=2
        failed2=returns[2][b'TraceLength']!=2
        #if failed2:
        #    print(returns[2][b'TraceLength'])
        failed3=returns[3][b'TraceLength']!=2
        #if failed3:
        #    print(returns[3][b'TraceLength'])
        failed4=returns[4][b'TraceLength']!=2
        #if failed4:
        #    print(returns[4][b'TraceLength'])
        return [failed0,failed1,failed2,failed3,failed4]
        
        
    def testRollingQuery(self):
        zInc=SeisGeometry[b'ZInc']
        passing=True
        for i in range(0,2001):
            z0=0+i*zInc
            z1=(1+i)*zInc
            returns=self.executeQueries(z0,z1)
            ret=self.checkRollingReturns(z0,z1,returns)
            passed=all(ret)
            if not passed:
                pass#print("Failed rolling at {} {} {}".format(z0,z1,ret))
            passing=passing and passed
        self.assertTrue(passing,"Failed rolling check")
            
    def testQueryType0(self):
        z0=SeisGeometry[b'MinZ']-SeisGeometry[b'ZInc']*5
        z1=SeisGeometry[b'MinZ']-SeisGeometry[b'ZInc']*3
        returns=self.executeQueries(z0,z1)
        #print("****TYPE 0 RETURNS*****")
        #print(returns)
        self.checkReturns0(z0,z1,returns)
    
    def testQueryType1(self):
        z0=SeisGeometry[b'MinZ']-SeisGeometry[b'ZInc']*5
        z1=SeisGeometry[b'MinZ']
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 1 RETURNS*****")
        #print(returns)
        self.checkReturns1(z0,z1,returns)
        
    def testQueryType2(self):
        z0=SeisGeometry[b'MinZ']-SeisGeometry[b'ZInc']*5
        z1=SeisGeometry[b'MinZ']+(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/2
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 2 RETURNS*****")
        #print(returns)
        self.checkReturns2(z0,z1,returns)


    def testQueryType3(self):
        z0=SeisGeometry[b'MinZ']
        z1=SeisGeometry[b'MinZ']+(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/2
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 3 RETURNS*****")
        #print(returns)
        #self.checkReturns3(z0,z1,returns)
        self.checkReturns3(z0,z1,returns)
        
    def testQueryType4(self):
        z0=SeisGeometry[b'MinZ']
        z1=SeisGeometry[b'MaxZ']
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 4 RETURNS*****")
        #print(returns)
        self.checkReturns4(z0,z1,returns)
        
    def testQueryType5(self):
        z0=SeisGeometry[b'MinZ']+(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/4
        z1=SeisGeometry[b'MaxZ']-(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/4
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 5 RETURNS*****")
        #print(returns)
        self.checkReturns5(z0,z1,returns)
        
    def testQueryType6(self):
        z0=SeisGeometry[b'MinZ']+(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/4
        z1=SeisGeometry[b'MaxZ']
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 6 RETURNS*****")
        #print(returns)
        self.checkReturns6(z0,z1,returns)
        
    def testQueryType7(self):
        z0=SeisGeometry[b'MinZ']+(SeisGeometry[b'MaxZ']-SeisGeometry[b'MinZ'])/4
        z1=SeisGeometry[b'MaxZ']+SeisGeometry[b'ZInc']*5
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 7 RETURNS*****")
        #print(returns)
        self.checkReturns7(z0,z1,returns)
        
    def testQueryType8(self):
        z0=SeisGeometry[b'MaxZ']
        z1=SeisGeometry[b'MaxZ']+SeisGeometry[b'ZInc']*5
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 8 RETURNS*****")
        #print(returns)
        self.checkReturns8(z0,z1,returns)
        
    def testQueryType9(self):
        z0=SeisGeometry[b'MaxZ']+SeisGeometry[b'ZInc']*3
        z1=SeisGeometry[b'MaxZ']+SeisGeometry[b'ZInc']*5
        returns=self.executeQueries(z0,z1)  
        #print("****TYPE 9 RETURNS*****")
        #print(returns)
        self.checkReturns9(z0,z1,returns)
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismicCollection",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismic",0))
#       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType0",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType1",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType2",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType3",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType4",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType5",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType6",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType7",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType8",0))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType9",0))
#       #suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testRollingQuery",0))
       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismicCollection",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismic",1))
#       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType0",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType1",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType2",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType3",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType4",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType5",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType6",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType7",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType8",1))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType9",1))
       #suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testRollingQuery",1))
       
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismicCollection",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismic",2))
       
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType0",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType1",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType2",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType3",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType4",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType5",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType6",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType7",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType8",2))
       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType9",2))
#       #suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testRollingQuery",2))
#       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismicCollection",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"createSeismic",3))
#       
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType0",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType1",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType2",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType3",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType4",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType5",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType6",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType7",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType8",3))
#       suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testQueryType9",3))
#       #suite.addTest(SeismicZBoundsQueryTestCase(server,repo,config,"testRollingQuery",3))
       
      
       return suite
            

def initModule(geodatasyncFn,idCompFn,trace):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    global __unittest
    __unittest=not trace
    
def getTestSuite(server,repo,config):
    return SeismicZBoundsQueryTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
   
   