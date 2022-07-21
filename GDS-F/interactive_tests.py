# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 10:39:25 2022
This file runs through the inetractive 'selection' tests. Requires
a PETREL project with each of the types in it to successfuly run through.
@author: lewthwju
"""

import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest
from tkinter import Tk
from tkinter import messagebox
from executor import TestExecutor



from test_utils import GDSErr 


GeoDataSync=None
IDComparison=None


class InteractiveTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,methodName):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
        
        
    def testSelectFolder(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Folder Test","Select a folder then click OK");
        folderID=GeoDataSync("getFolderIDSel",self.server)
        self.assertFalse(folderID==0,GDSErr(self.server,"Failed getFolderIDSel"))
        msg="Confirm selected folder is {}".format(str(folderID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong folder identified as selected")
    
    def testSelectInterpretationCollection(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Interpretation Collection Test","Select an interpretation collection then click OK");
        icID=GeoDataSync("getInterpretationCollectionIDSel",self.server)
        self.assertFalse(icID==0,GDSErr(self.server,"Failed getInterpretationCollectionIDSel"))
        msg="Confirm selected interpretation collection is {}".format(str(icID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong interpretation collection identified as selected")
    
    def testSelectSeismicCollection(self):  
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Seismic Collection Test","Select a seismic collection then click OK");
        seisID=GeoDataSync("getSeisColIDSel",self.server)
        print(seisID)
        self.assertFalse(seisID==0,GDSErr(self.server,"Failed get3DSeisColIDSel"))
        msg="Confirm selected seismic collection is {}".format(str(seisID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong Seismic Collection identified as selected")
        
    def testSelect3DSeismic(self):  
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 3D Seismic Test","Select a 3D seismic then click OK");
        seisID=GeoDataSync("get3DSeisIDSel",self.server)
        self.assertFalse(seisID==0,GDSErr(self.server,"Failed get3DSeisIDSel"))
        msg="Confirm selected seismic is {}".format(str(seisID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong 3D Seismic identified as selected")
        
    def testSelect3DSeisIntersection(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 3D Seismic Intersection Test","Select 3D Seismic Intersection (Inline,Crossline or Z");
        interID=GeoDataSync("getSeis3DIntersectionIDSel",self.server)
        self.assertFalse(interID==0,GDSErr(self.server,"Failed getSeis3DIntersectionIDSel"))
        msg="Confirm selected intersection is {}".format(str(interID[b"IntersectionID"][0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong intersection identified as selected")
        
    def testSelect2DSeisLine(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 2D Seismic Line Test","Select a 2D Seismic Line");
        lineID=GeoDataSync("get2DSeisIDSel",self.server)
        self.assertFalse(lineID==0,GDSErr(self.server,"Failed get2DSeisIDSel"))
        msg="Confirm selected line is {}".format(str(lineID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong 2D Line identified as selected")
        
    def testSelectSurface(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Surface Test","Select a surface");
        surfID=GeoDataSync("getSurfIDSel",self.server)
        self.assertFalse(surfID==0,GDSErr(self.server,"Failed getSurfIDSel"))
        msg="Confirm selected surface is {}".format(str(surfID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong surface identified as selected")
        
    def testSelectSurfaceProperty(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Surface Property Test","Select a surface property");
        surfPropID=GeoDataSync("getSurfPropIDSel",self.server)
        self.assertFalse(surfPropID==0,GDSErr(self.server,"Failed getSurfPropIDSel"))
        msg="Confirm selected surface property is {}".format(str(surfPropID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong surface property identified as selected")
     
    def testSelect3DHorizon(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 3D Horizon Test","Select a 3D Horizon");
        horzID=GeoDataSync("get3DHorzIDSel",self.server)
        self.assertFalse(horzID==0,GDSErr(self.server,"Failed get3DHorzIDSel"))
        msg="Confirm selected 3D Horizon is {}".format(str(horzID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong 3D horizon identified as selected")
    
    def testSelect3DHorizonProperty(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 3D Horizon Property Test","Select a 3D Horizon Property");
        horzPropID=GeoDataSync("get3DHorzPropIDSel",self.server)
        self.assertFalse(horzPropID==0,GDSErr(self.server,"Failed get3DHorzPropIDSel"))
        msg="Confirm selected 3D Horizon property is {}".format(str(horzPropID[b"HorzPropID"][0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong 3D horizon property identified as selected")
        
    def testSelect2DHorizon(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select 2D Horizon Test","Select a 2D Horizon");
        horzID=GeoDataSync("get2DHorzIDSel",self.server)
        self.assertFalse(horzID==0,GDSErr(self.server,"Failed get2DHorzIDSel"))
        msg="Confirm selected 2D Horizon is {}".format(str(horzID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong 2D horizon identified as selected")
    
    def testSelectWell(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Well Test","Select a well");
        wellID=GeoDataSync("getWellIDSel",self.server)
        self.assertFalse(wellID==0,GDSErr(self.server,"Failed getWellIDSel"))
        msg="Confirm selected well is {}".format(str(wellID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong well identified as selected")    
    
    def testSelectWellCollection(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Well Collection Test","Select a well collection");
        wellColID=GeoDataSync("getWellCollectionIDSel",self.server)
        self.assertFalse(wellColID==0,GDSErr(self.server,"Failed getWellCollectionIDSel"))
        msg="Confirm selected well collection is {}".format(str(wellColID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong well collection identified as selected")
        
    def testSelectLog(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Log Test","Select a well log");
        logID=GeoDataSync("getLogIDSel",self.server)
        self.assertFalse(logID==0,GDSErr(self.server,"Failed getLogIDSel"))
        msg="Confirm selected well log is {}".format(str(logID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong well log identified as selected")   
        
    def testSelectGlobalLog(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Global Log Test","Select a Global well log");
        logID=GeoDataSync("getGlobalLogIDSel",self.server)
        self.assertFalse(logID==0,GDSErr(self.server,"Failed getLogIDSel"))
        msg="Confirm selected global well log is {}".format(str(logID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong global well log identified as selected")   
        
        
    def testSelectWavelet(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Wavelet Test","Select a wavelet");
        wavID=GeoDataSync("getWaveletIDSel",self.server)
        self.assertFalse(wavID==0,GDSErr(self.server,"Failed getWaveletIDSel"))
        msg="Confirm selected wavelet is {}".format(str(wavID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong wavelet identified as selected") 
        
    def testSelectFault(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Fault Test","Select a fault");
        faultID=GeoDataSync("getFaultIDSel",self.server)
        self.assertFalse(faultID==0,GDSErr(self.server,"Failed getFaultIDSel"))
        msg="Confirm selected fault is {}".format(str(faultID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong fault identified as selected") 
        
    def testSelectPointSet(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select PointSet Test","Select a pointset");
        psID=GeoDataSync("getPointSetIDSel",self.server)
        self.assertFalse(psID==0,GDSErr(self.server,"Failed getPointSetIDSel"))
        msg="Confirm selected PointSet is {}".format(str(psID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong pointset identified as selected")
        
    def testSelectPolygon(self):
        master=Tk()
        master.withdraw()
        messagebox.showinfo("Select Polygon Test","Select a polygon");
        polyID=GeoDataSync("getPolygonIDSel",self.server)
        self.assertFalse(polyID==0,GDSErr(self.server,"Failed getPolygonIDSel"))
        msg="Confirm selected Polygon is {}".format(str(polyID[0],"utf-8"))
        ret=messagebox.askyesno("Yes|No",msg)
        self.assertTrue(ret,"Wrong polygon identified as selected")

    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectFolder"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectInterpretationCollection"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectSeismicCollection"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectGlobalLog"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect3DSeismic"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect3DSeisIntersection"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect2DSeisLine"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectSurface"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect3DHorizon"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect3DHorizonProperty"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelect2DHorizon"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectWell"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectWellCollection"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectLog"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectWavelet"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectFault"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectPointSet"))
       suite.addTest(InteractiveTestCase(server,repo,config,"testSelectPolygon"))
       return suite
   
def initModule(geodatasyncFn,idCompFn,trace):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    global __unittest
    __unittest=not trace
    
def getTestSuite(server,repo,config):
    return InteractiveTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
   