# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:07:03 2022

@author: lewthwju
"""
import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest



from executor import TestExecutor

from test_utils import compareFloatLists    
from test_utils import IDInList
from test_utils import GDSErr 


from constants import SEISMIC_COL_0
from constants import WAVELET_0


GeoDataSync=None
IDComparison=None
 
 



class WaveletTestCase(unittest.TestCase):
    def __init__(self,server,repo,config,method):
        super().__init__(method)
        self.server=server
        self.config=config
        self.repo=repo

    def testCreateWavelet(self):
        seisColID=self.repo.getSeismicCollectionID(SEISMIC_COL_0)
        if seisColID==None:
            self.skipTest("Required Seismic Collection with asset repository name '{}' not found".format(SEISMIC_COL_0))
        wlID=self.repo.createWavelet(WAVELET_0,seisColID)
        self.assertFalse(wlID==None or wlID==0,GDSErr(self.server,"Failed createWavelet at top level"))
    
    def testPutWaveletData(self):
        wlID=self.repo.getWaveletID(WAVELET_0)
        data=self.config.getWaveletData()
        success=GeoDataSync("putWaveletData",self.server,wlID,data["SampleInt"],data["Wavelet"])
        self.assertTrue(success==1,GDSErr(self.server,"Failed GDS call to putPointSetData"))
    
    def testGetWaveletData(self):
        wlID=self.repo.getWaveletID(WAVELET_0)
        knowndata=self.config.getWaveletData()
        data=GeoDataSync("getWaveletData",self.server,wlID)
        self.assertFalse(data is None or data==0,GDSErr(self.server,"Failed GDS call to getPointSetData"))
        self.assertEquals(data[b"SampleInterval"],knowndata["SampleInt"],"SampleInterval does not match in getWaveletData")
        self.assertTrue(compareFloatLists(data[b"Data"],knowndata["Wavelet"]),"Data does not match in getWaveletData")
       
        
 
            
    def getTestSuite(server,repo,config):
        suite=unittest.TestSuite()
        suite.addTest(WaveletTestCase(server,repo,config,"testCreateWavelet"))
        suite.addTest(WaveletTestCase(server,repo,config,"testPutWaveletData"))
        suite.addTest(WaveletTestCase(server,repo,config,"testGetWaveletData"))
       
        return suite
    
    
  
def initModule(geodatasyncFn,idCompFn):
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    
def getTestSuite(server,repo,config):
    return WaveletTestCase.getTestSuite(server, repo, config)
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
    
    
    