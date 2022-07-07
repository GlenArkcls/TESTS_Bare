# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:52:26 2022

This module is for test functions concerned with normal operation of 3D and 2D seismics

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
from test_utils import bilinearTraceInterp


from constants import SEISMIC_COL_0
from constants import SEISMIC_COL_1
from constants import SEISMIC3D_0
from constants import SEISMIC2D_0

GeoDataSync=None
IDComparison=None


class SeismicTestCase(unittest.TestCase):

    def __init__(self,server,repo,config,methodName):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
   
    
    def testCreateSeismicCollection(self):
        seisColID=self.repo.createSeismicCollection(SEISMIC_COL_0)
        self.assertFalse(seisColID is None or seisColID==0,GDSErr(self.server,"Failed to create Seismic Collection:"))
    
    def testGetSeisColIDList(self):
        seisColIDList=GeoDataSync("getSeisColIDList",self.server)
        self.assertFalse(seisColIDList is None or seisColIDList==0,GDSErr(self.server,"Failed GDS call to getSeisColIDList."))
        
    def testVerifySeismicCollection(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        seisColIDList=GeoDataSync("getSeisColIDList",self.server)
        
        self.assertFalse(seisColID is None or seisColID==0,GDSErr(self.server,"Failed GDS call to getSeisColIDList"))
        self.assertTrue(IDInList(IDComparison,seisColID,seisColIDList),"created seismic collection not found in collection list")
          
    def testCreate3DSeismic(self):
        args=[self.repo.getSeismicCollectionID(SEISMIC_COL_0)]
        geom=makeCreationGeometryFromFullGeometry(self.config.get3DSeismicGeometry(False))
        args.extend(list(geom.values()))
        seisID=self.repo.create3DSeismic(SEISMIC3D_0,*args);
        self.assertFalse(seisID is None or seisID==0,GDSErr(self.server,"Failed create3DSeismic"))
        
        
    def testGet3DSeisIDList(self):
        colList=GeoDataSync("get3DSeisIDList",self.server)
        self.assertFalse(colList is None or colList==0,GDSErr(self.server,"Failed GDS call to get3DSeisIDList"))
       
    def testVerify3DSeismicInCollection(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        colList=GeoDataSync("get3DSeisIDListCol",self.server,seisColID)
        seisCol=self.repo.get3DSeismicID(SEISMIC3D_0)
        self.assertFalse(colList==None or colList==0,GDSErr(self.server,"Failed GDS call to get3DSeisIDListCol"))
        self.assertTrue(IDInList(IDComparison,seisCol,colList),"Test seismic did not appear in collection list")
    
    def testGetGeometry(self):
        seisGeom=GeoDataSync("get3DSeisGeom",self.server,self.repo.get3DSeismicID(SEISMIC3D_0))
        self.assertFalse(seisGeom is None or seisGeom==0,GDSErr(self.server,"Failed GDS call get3DSeisGeom"))
        testGeom=self.config.get3DSeismicGeometry(False)
        for k in testGeom.keys():
            with self.subTest(k=k):
                self.assertAlmostEqual(seisGeom[k],testGeom[k],4)
        
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
         
    def testGet3DSeisDataRange(self):
        volumeData=self.config.get3DSeismicData()
        minvalue=sys.float_info.max
        maxvalue=sys.float_info.min
        for l in volumeData:
            tmin=min(l)
            tmax=max(l)
            if tmin<minvalue:
                minvalue=tmin
            if tmax>maxvalue:
                maxvalue=tmax
        minmax=GeoDataSync("get3DSeisDataRange",self.server,self.repo.get3DSeismicID(SEISMIC3D_0))
        self.assertFalse(minmax==None or minmax==0,GDSErr(self.server,"Failed GDS call to get3DSeisDataRange"))
        self.assertAlmostEqual(minvalue,minmax[b'MinValue'],4,"Minimum value mismatch, {} {}".format(minvalue,minmax[b'MinValue']))
        self.assertAlmostEqual(maxvalue,minmax[b'MaxValue'],4,"Maximum value mismatch, {} {}".format(maxvalue,minmax[b'MaxValue']))
    
    def testGet3DSeisTracesAll(self):
        geom=self.config.get3DSeismicGeometry(False)
        '''
        Trim the z's by a sample at top and base to ensure
        correct handling of that aspect
        '''
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=minZ+incZ
        maxZ=maxZ-incZ
        volumeData=self.config.get3DSeismicData()
        gotData=GeoDataSync("get3DSeisTracesAll",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesAll"))
        returnedTraces=gotData[b'Traces']
        self.assertTrue(len(returnedTraces)==len(volumeData)-2,"No. samples mismatch in returned data from get3DSeisTracesAll")
        self.assertTrue(len(returnedTraces[0])==len(volumeData[0]),"No. of traces mismatch in returned data from get3DSeisTracesAll")
        for i in range(len(returnedTraces)):
             with self.subTest(i=i):
                 self.assertTrue(compareFloatLists(volumeData[i+1],returnedTraces[i]),"Mismatched data in trace in get3DSeisTracesAll")
                 
    def testGet3DSeisTracesAllSampleCountTest(self):
        geom=self.config.get3DSeismicGeometry(False)
        '''
        Trim the z's by a sample at top and base to ensure
        correct handling of that aspect
        '''
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=3.000
        maxZ=3.000+4*incZ
        print(minZ,maxZ)
        gotData=GeoDataSync("get3DSeisTracesAll",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesAll"))
        returnedTraces=gotData[b'Traces']
        print(gotData[b'Z0'])
        self.assertTrue(len(returnedTraces)==5,"No. samples mismatch in returned data from get3DSeisTracesAll")
       
        
        
    def testGet3DSeisValuesSpec(self):
         geom=self.config.get3DSeismicGeometry(False)
         '''
         Trim the z's by a sample at top and base to ensure
          correct handling of that aspect
        '''
         minZ=geom[b"MinZ"]
         maxZ=geom[b"MaxZ"]
         incZ=geom[b"ZInc"]
         minZ=minZ+incZ
         maxZ=maxZ-incZ
         
         volumeData=self.config.get3DSeismicData()
         ilines,xlines=geom.get3DGeometryILXLPairs()
         
         gotData=GeoDataSync("get3DSeisTracesSpec",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),ilines,xlines,minZ,maxZ)
         self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesSpec"))
         returnedTraces=gotData[b'Traces']
         
         self.assertTrue(len(returnedTraces)==len(volumeData)-2,"No. samples mismatch in returned data from get3DSeisTracesSpec")
         self.assertTrue(len(returnedTraces[0])==len(volumeData[0]),"No. of traces mismatch in returned data from get3DSeisTracesSpec")
         for i in range(len(returnedTraces)):
             with self.subTest(i=i):
                 self.assertTrue(compareFloatLists(volumeData[i+1],returnedTraces[i]),"Mismatched data in trace in get3DSeisTracesSpec")
                 
    ''' 
    Get the values from the volume expressed by the ranges. 
    '''
    def testGet3DSeisTracesRange(self):
        geom=self.config.get3DSeismicGeometry(False)
        '''
        Trim the z's by a sample at top and base to ensure
        correct handling of that aspect
        '''
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=minZ+incZ
        maxZ=maxZ-incZ
        gotData=GeoDataSync("get3DSeisTracesRange",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),geom[b"MinInline"],geom[b"MaxInline"],geom[b"MinXline"],geom[b"MaxXline"],minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesRange:"))
        returnedTraces=gotData[b'Traces']
        volumeData=self.config.get3DSeismicData()
        self.assertTrue(len(returnedTraces)==len(volumeData)-2,"No. samples mismatch in returned data from get3DSeisTracesRange")
        self.assertTrue(len(returnedTraces[0])==len(volumeData[0]),"No. of traces mismatch in returned data from get3DSeisTracesRange")
        for i in range(len(returnedTraces)):
             with self.subTest(i=i):
                 self.assertTrue(compareFloatLists(volumeData[i+1],returnedTraces[i]),"Mismatched data in trace")
    '''
    Test getting all the data from an inline of the volume
    We choose the inline in the middle of the volume to test - perhaps a couple chosen at random would
    be better?
    Volume is assumed to be complete - ie no missing traces (even if they are filled with NaNs)
    '''      
    def testGet3DSeisTracesInXIInline(self):
        geom=self.config.get3DSeismicGeometry(False)
       
        ilCount=round((geom[b'MaxInline']-geom[b'MinInline'])/geom[b'InlineInc'])+1
        xlCount=round((geom[b'MaxXline']-geom[b'MinXline'])/geom[b'XlineInc'])+1
        ilix=round(ilCount/2)#index of inline
        il=geom[b"MinInline"]+ilix*geom[b"InlineInc"]#actual inline
        '''
        Trim the z's by a sample at top and base to ensure
        correct handling of that aspect
        '''
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=minZ+incZ
        maxZ=maxZ-incZ
        gotData=GeoDataSync("get3DSeisTracesInXl",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),1,il,minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesRange:"))
        self.assertEqual(len(gotData[b"Inlines"]),xlCount,"Incorrect no. of inlines returned from get3DSeisTracesInXl (inlines)")
        self.assertEqual(len(gotData[b'Xlines']),xlCount,"Incorrect no. of crosslines returned from get3DSeisTracesInXl (inlines)")
        returnedTraces=gotData[b'Traces']
        volumeData=self.config.get3DSeismicData()
        self.assertTrue(len(returnedTraces)==len(volumeData)-2,"No. samples mismatch in returned data from get3DSeisTracesInXl (Inline)")
        ix0=ilix*xlCount#first trace index in volume
        ix1=ix0+xlCount#last plus one index
        for i in range(len(returnedTraces)):
             with self.subTest(i=i):
                 self.assertTrue(compareFloatLists(volumeData[i+1][ix0:ix1],returnedTraces[i]),"Mismatched data in trace")
    '''
    Test getting all the data from a crossline of the volume
    We choose the crossline in the middle of the volume to test - perhaps a couple chosen at random would
    be better?
    Volume is assumed to be complete - ie no missing traces (even if they are filled with NaNs)
    '''
    def testGet3DSeisTracesInXICrossline(self):
        geom=self.config.get3DSeismicGeometry(False)
       
        ilCount=round((geom[b'MaxInline']-geom[b'MinInline'])/geom[b'InlineInc'])+1
        xlCount=round((geom[b'MaxXline']-geom[b'MinXline'])/geom[b'XlineInc'])+1
        xlix=round(xlCount/2)#index of xline
        xl=geom[b"MinXline"]+xlix*geom[b"XlineInc"]#actual xline
        '''
        Trim the z's by a sample at top and base to ensure
        correct handling of that aspect
        '''
        minZ=geom[b"MinZ"]
        maxZ=geom[b"MaxZ"]
        incZ=geom[b"ZInc"]
        minZ=minZ+incZ
        maxZ=maxZ-incZ
        gotData=GeoDataSync("get3DSeisTracesInXl",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),0,xl,minZ,maxZ)
        self.assertFalse(gotData==None or gotData==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesInXl (crosslines)"))
        self.assertEqual(len(gotData[b"Inlines"]),ilCount,"Incorrect no. of inlines returned from get3DSeisTracesInXl (crosslines)")
        self.assertEqual(len(gotData[b'Xlines']),ilCount,"Incorrect no. of crosslines returned from get3DSeisTracesInXl (crosslines)")
        returnedTraces=gotData[b'Traces']
        volumeData=self.config.get3DSeismicData()
        self.assertTrue(len(returnedTraces)==len(volumeData)-2,"No. samples mismatch in returned data from get3DSeisTracesInXl (Crossline)")
        il0=xlix#first trace index in volume
        il1=il0+xlCount*(ilCount-1)+1#last plus one index
        for i in range(len(returnedTraces)):
             with self.subTest(i=i):
                 self.assertTrue(compareFloatLists(volumeData[i+1][il0:il1:xlCount],returnedTraces[i]),"Mismatched data in trace")
    
    #@unittest.skip("Test not run due to known errors")
    def testGet3DSeisTracesTransect(self):
        geom=self.config.get3DSeismicGeometry()
        seisID = self.repo.get3DSeismicID(SEISMIC3D_0)
        x0 = geom[b'X0']+25+24
        y0 = geom[b'Y0']+24
        x1 = geom[b'X0']+25+24
        y1 = geom[b'Y0']+124
        minZ = geom[b'MinZ']
        maxZ = geom[b'MinZ']+geom[b'ZInc'] #geom[b'MaxZ']
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
            #print(ilxl)
            #print(xy)
        ilrange=geom.getInlineRange();
        xlrange=geom.getCrosslineRange();
        interpTraces=[]
        for ilxl in ilxls:
            nil=getNearestIntegerInRange(ilrange,ilxl[0])
            nxl=getNearestIntegerInRange(xlrange,ilxl[1])
            if nil>ilxl[0]:
                sil=nil-geom.getInlineInc()
                lil=nil
            else:
                sil=nil
                lil=nil+geom.getInlineInc()
            if nxl>ilxl[1]:
                sxl=nxl-geom.getXlineInc()
                lxl=nxl
            else:
                sxl=nxl
                lxl=nxl+geom.getXlineInc()
            traces=GeoDataSync("get3DSeisTracesRange",self.server,seisID,sil,lil,sxl,lxl,minZ,maxZ)
            distIL=(ilxl[0]-sil)/geom.getInlineInc();
            distXL=(ilxl[1]-sxl)/geom.getXlineInc();
            #print("in {} {} {}".format(nil,sil,lil))
            #print(traces)
            #print(distIL)
            #print(distXL)
            interpTrace=bilinearTraceInterp(distIL,distXL,traces[b'Traces'])
            interpTraces.append(interpTrace)
        #print(interpTraces)
        reshapedInterps=[[interpTraces[i][j] for i in range(0,len(interpTraces))] for j in range(0,len(interpTraces[0]))]
        #print(reshapedInterps)
        seisTransect = GeoDataSync("get3DSeisTracesTransect",self.server, seisID, x0, y0, x1, y1, minZ, maxZ, numTraces)
        self.assertFalse(seisTransect==None or seisTransect==0,GDSErr(self.server,"Failed GDS call to get3DSeisTracesTransect"))
        nTraces = seisTransect[b'NumTraces']
        tracesLength = seisTransect[b'TraceLength']
        #print(seisTransect)
        self.assertFalse(nTraces==None or nTraces==0,GDSErr(self.server,"Incorrect no. of Traces from get3DSeisTracesTransect"))
        self.assertFalse(tracesLength==None or tracesLength==0,GDSErr(self.server,"Incorrect Traces length from get3DSeisTracesTransect"))
        for i in range(0,tracesLength):
                self.assertTrue(compareFloatLists(seisTransect[b'Traces'][i],reshapedInterps[i]),"get3DSeisTracesTransect data values do not match")
        
    
    def testGetInlineCrosslineFromXY(self):
        geom=self.config.get3DSeismicGeometry(False)
        ilines=geom.getInlineList()
        xlines=geom.getCrosslineList()
        ils=[float(x) +0.7 for x in ilines[0:len(ilines):3]]
        xls=[float(x) +0.3 for x in xlines[0:len(xlines):3]]
        ilxls=list(zip(ils,xls))
       
        coordsFromGeom=[geom.transformILXL(ilxl) for ilxl in ilxls]
        xcoords=[x[0] for x in coordsFromGeom]
        ycoords=[x[1] for x in coordsFromGeom]
        ilsRange=range(geom.getMinInline(),geom.getMaxInline()+1,geom.getInlineInc())
        xlsRange=range(geom.getMinXline(),geom.getMaxXline()+1,geom.getXlineInc())
        testIls=[getNearestIntegerInRange(ilsRange,x[0]) for x in ilxls]
        testXls=[getNearestIntegerInRange(xlsRange,x[1]) for x in ilxls]
        ilxlsret=GeoDataSync("getInlineCrosslineFromXY",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),xcoords,ycoords)
        self.assertFalse(ilxlsret==0,GDSErr(self.server,"Failed call to getInlineCrosslineFromXY"))
        self.assertTrue(compareFloatLists(ilxlsret[b'Inlines'],testIls),GDSErr(self.server,"Inlines from transform not correct"))
        self.assertTrue(compareFloatLists(ilxlsret[b'Xlines'],testXls),GDSErr(self.server,"Crosslines from transform not correct"))
        
    
    def testGetInlineCrosslineFromXYExact(self):
        geom=self.config.get3DSeismicGeometry(False)
        ilines=geom.getInlineList()
        xlines=geom.getCrosslineList()
        ils=[float(x) +0.7 for x in ilines[0:len(ilines):3]]
        xls=[float(x) +0.3 for x in xlines[0:len(xlines):3]]
        ilxls=list(zip(ils,xls))
        ils=[x[0] for x in ilxls]
        xls=[x[1] for x in ilxls]
        coordsFromGeom=[geom.transformILXL(ilxl) for ilxl in ilxls]
        xcoords=[x[0] for x in coordsFromGeom]
        ycoords=[x[1] for x in coordsFromGeom]
        ilxlsret=GeoDataSync("getInlineCrosslineFromXYExact",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),xcoords,ycoords)
        self.assertFalse(ilxlsret==0,GDSErr(self.server,"Failed call to getInlineCrosslineFromXYExact"))
        self.assertTrue(compareFloatLists(ilxlsret[b'Inlines'],ils),GDSErr(self.server,"Inlines from transform not correct"))
        self.assertTrue(compareFloatLists(ilxlsret[b'Xlines'],xls),GDSErr(self.server,"Crosslines from transform not correct"))
        
   
    def testGetXYFromInlineCrossline(self):
        geom=self.config.get3DSeismicGeometry(False)
        ilines=geom.getInlineList()
        xlines=geom.getCrosslineList()
        ils=[float(x) for x in ilines[0:len(ilines):3]]
        xls=[float(x) for x in xlines[0:len(xlines):3]]
        ilxls=list(zip(ils,xls))
        ils=[x[0] for x in ilxls]
        xls=[x[1] for x in ilxls]
        coordsFromGeom=[geom.transformILXL(ilxl) for ilxl in ilxls]
        xcoords=[x[0] for x in coordsFromGeom]
        ycoords=[x[1] for x in coordsFromGeom]
       
        coords=GeoDataSync("getXYFromInlineCrossline",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),ils,xls)
        self.assertFalse(coords==0,GDSErr(self.server,"Failed call to getXYFromInlineCrossline"))
        self.assertTrue(compareFloatLists(xcoords,coords[b'XCoords']),GDSErr(self.server,"Coordinates from transform not correct"))
        self.assertTrue(compareFloatLists(ycoords,coords[b'YCoords']),GDSErr(self.server,"Coordinates from transform not correct"))
    '''
    This is not in fact logically as good a test as it might appear. 
    It effectively does AA^-1 which equals I. In other words the round trip
    could produce the output that matches input without the actual transform 
    (A) being correct, or indeed anything other than invertible - depends on the target impl.
    '''
    def testCoordinateTransformRoundTrip(self):
        #Lets do a combo of every 3rd il/xl
        geom=self.config.get3DSeismicGeometry(False)
        ilines=geom.getInlineList()
        xlines=geom.getCrosslineList()
        arlen=min(len(ilines),len(xlines))
        ils=[float(x) for x in ilines[0:arlen:3]]
        xls=[float(x) for x in xlines[0:arlen:3]]

        coords=GeoDataSync("getXYFromInlineCrossline",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),ils,xls)
        
        self.assertFalse(coords==None or coords==0,GDSErr(self.server,"Failed GDS call to getXYFromInlineCrossline"))
        ilxl=GeoDataSync("getInlineCrosslineFromXY",self.server,self.repo.get3DSeismicID(SEISMIC3D_0),coords[b'XCoords'],coords[b'YCoords'])
        self.assertFalse(ilxl is None or ilxl==0,"Failed GDS call to getInlineCrosslineFromXY")
        self.assertTrue(compareFloatLists(ilxl[b'Inlines'],ils),"Output inlines do not match input from coordinate transform round trip")
        self.assertTrue(compareFloatLists(ilxl[b'Xlines'],xls),"Output crosslines do not match input from coordinate transform round trip")
        
        
    '''
    We need a separate collection for the 2D seismic
    '''
    def testCreateSeismicCollectionFor2D(self):
        seisColID=self.repo.createSeismicCollection(SEISMIC_COL_1)
        self.assertFalse(seisColID==None or seisColID==0,GDSErr(self.server,"Failed to get create seismic collection for 2D"))
    
    def testCreate2DSeismic(self):
        geom=self.config.get2DSeismicGeometry(False)
        args=list(geom.values())
        args.append(self.repo.getSeismicCollectionID(SEISMIC_COL_1))
        seisID=self.repo.create2DSeismic(SEISMIC2D_0,*args)
        self.assertFalse(seisID is None or seisID==0,GDSErr(self.server,"Failed create2DSeismic"))
    
    '''
    Note the name in the ID comes back with '[Seismic 2D Line]' 
    '''
    def testGet2DSeisIDList(self):
        seisIDList=GeoDataSync("get2DSeisIDList",self.server)
        self.assertFalse(seisIDList is None or seisIDList==0,GDSErr(self.server,"Failed GDS call to get2DSeisIDList"))
        self.assertTrue(IDInList(IDComparison,self.repo.get2DSeismicID(SEISMIC2D_0),seisIDList),"2D Seismic not found in 2D Seismic ID list")
    '''
    Note the name in the ID comes back with '[Seismic 2D Line]' appended to it from PETREL
    for this reason we check equality of the droid only
    '''   
    def testVerify2DSeismicInCollection(self):
        seisIDList=GeoDataSync("get2DSeisIDListCol",self.server,self.repo.getSeismicCollectionID(SEISMIC_COL_1))
        self.assertFalse(seisIDList==None or seisIDList==0,GDSErr(self.server,"Failed in GDS call to get2DSeisIDListCol"))
        self.assertTrue(IDInList(IDComparison,self.repo.get2DSeismicID(SEISMIC2D_0),seisIDList),"2D Seismic not found in 2D Seismic ID list")
        
    def testGet2DSeisGeom(self):
        geom=GeoDataSync("get2DSeisGeom",self.server,self.repo.get2DSeismicID(SEISMIC2D_0))
        self.assertFalse(geom is None or geom==0,GDSErr(self.server,"Failed GDS call to get2DSeisGeom"))
        knowngeom=self.config.get2DSeismicGeometry(False)
        self.assertTrue(compareFloatLists(geom[b'XCoords'],knowngeom[b'XCoords']),"Mismatched XCoords from GDS get2DSeisGeom")
        self.assertTrue(compareFloatLists(geom[b'YCoords'],knowngeom[b'YCoords']),"Mismatched YCoords from GDS get2DSeisGeom")
        self.assertEqual(geom[b'isDepth'],knowngeom[b'isDepth'],"Mismatched isDepth from GDS  get2DSeisGeom")
        self.assertAlmostEqual(geom[b'MinZ'],knowngeom[b'MinZ'],4,"Mismatched MinZ from GDS  get2DSeisGeom")
        self.assertAlmostEqual(geom[b'MaxZ'],knowngeom[b'ZInc']*(knowngeom[b'TraceLength']-1)+knowngeom[b'MinZ'],4,"Mismatched MaxZ from GDS  get2DSeisGeom")
        
        
    def testPut2DSeisTraces(self):
        ret=GeoDataSync("put2DSeisTraces",self.server,self.repo.get2DSeismicID(SEISMIC2D_0),self.config.get2DLineData())
        self.assertTrue(ret==1,GDSErr(self.server,"Failed GDS call to put2DSeisTraces"))
        
    def testGet2DSeisDataRange(self):
        lineData=self.config.get2DLineData()
        minvalue=sys.float_info.max
        maxvalue=sys.float_info.min
        for l in lineData:
            tmin=min(l)
            tmax=max(l)
            if tmin<minvalue:
                minvalue=tmin
            if tmax>maxvalue:
                maxvalue=tmax
        minmax=GeoDataSync("get2DSeisDataRange",self.server,self.repo.get2DSeismicID(SEISMIC2D_0))
        self.assertFalse(minmax==None or minmax==0,GDSErr(self.server,"Failed GDS call to get2DSeisDataRange"))
        self.assertAlmostEqual(minvalue,minmax[b'MinValue'],4,"Minimum value mismatch, {} {}".format(minvalue,minmax[b'MinValue']))
        self.assertAlmostEqual(maxvalue,minmax[b'MaxValue'],4,"Maximum value mismatch, {} {}".format(maxvalue,minmax[b'MaxValue']))
        
    def testGet2DSeisTracesAll(self):
        gotData=GeoDataSync("get2DSeisTracesAll",self.server,self.repo.get2DSeismicID(SEISMIC2D_0))
        self.assertFalse(gotData is None or gotData==0,GDSErr(self.server,"Failed GDS call to get2DSeisTracesAll"))
        lineData=self.config.get2DLineData()
        traceData=gotData[b'Traces']
        self.assertTrue(len(traceData)==len(lineData),"Mismatched no of traces from get2DSeisTracesAll")
        for i in range(len(traceData)):
            self.assertTrue(compareFloatLists(traceData[i],lineData[i]))
    
    '''
    Check every second trace
    '''          
    def testGet2DSeisTracesSpec(self):
        lineData=self.config.get2DLineData()
        ix=[x+1 for x in range(len(lineData[0])) if x%2==0]
        gotData=GeoDataSync("get2DSeisTracesSpec",self.server,self.repo.get2DSeismicID(SEISMIC2D_0),ix)
        self.assertFalse(gotData is None or gotData==0,GDSErr(self.server,"Failed GDS call to get2DSeisTracesSpec"))
        traceData=gotData[b'Traces']
        self.assertTrue(len(traceData)==len(lineData),"Mismatched no of samples from get2DSeisTracesSpec")
        self.assertTrue(len(traceData[0])==len(ix),"Mismatched no of traces from get2DSeisTracesSpec")
        for i in range(len(traceData)):
            with self.subTest(i=i):
                self.assertTrue(compareFloatLists(traceData[i],lineData[i][0:len(lineData[0])+1:2]))
        
        
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
       suite.addTest(SeismicTestCase(server,repo,config,"testCreateSeismicCollection"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGetSeisColIDList"))
       suite.addTest(SeismicTestCase(server,repo,config,"testVerifySeismicCollection"))
       suite.addTest(SeismicTestCase(server,repo,config,"testCreate3DSeismic"))
      
       suite.addTest(SeismicTestCase(server,repo,config,"testVerify3DSeismicInCollection"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisIDList"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGetGeometry"))
       
       suite.addTest(SeismicTestCase(server,repo,config,"testPut3DSeisTraces"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisDataRange"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesAll"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesAllSampleCountTest"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisValuesSpec"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesRange"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesInXIInline"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesInXICrossline"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet3DSeisTracesTransect"))
       
       suite.addTest(SeismicTestCase(server,repo,config,"testGetInlineCrosslineFromXY"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGetInlineCrosslineFromXYExact"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGetXYFromInlineCrossline"))
       suite.addTest(SeismicTestCase(server,repo,config,"testCoordinateTransformRoundTrip"))
       
       suite.addTest(SeismicTestCase(server,repo,config,"testCreateSeismicCollectionFor2D"))
       suite.addTest(SeismicTestCase(server,repo,config,"testCreate2DSeismic"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet2DSeisIDList"))
       suite.addTest(SeismicTestCase(server,repo,config,"testVerify2DSeismicInCollection"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet2DSeisGeom"))
       suite.addTest(SeismicTestCase(server,repo,config,"testPut2DSeisTraces"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet2DSeisDataRange"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet2DSeisTracesAll"))
       suite.addTest(SeismicTestCase(server,repo,config,"testGet2DSeisTracesSpec"))
      
       return suite
            

def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return SeismicTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
   
   