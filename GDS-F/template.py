# -*- coding: utf-8 -*-
"""
This module is a template for producing new files of tests. This can either be
an acvtual test file - in which case one (or more) test classes implementing
tests should be implemented here, or it aggregates tests from other files, 
in which case these modules are imported and their tests gathered together
into one suite. 
Whilst it is possible to have more than one test class in a file, and we can
mix the aggregation vs test class in a single file, neither is recommended or
gives much value. Sticking to either a single test class in a file OR an
aggregation of other modules tests (which can themselves be aggregates) leads
to more modular and cleaner structure.

Created on Tue Mar 15 14:52:26 2022



@author: lewthwju
"""
import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest
from executor import TestExecutor

#Keep the utility functions that you need
from test_utils import compareFloatLists    
from test_utils import makeCreationGeometryFromFullGeometry 
from test_utils import IDInList
from test_utils import GDSErr 


#Import the constants that you need
from constants import SEISMIC_COL_0
from constants import SEISMIC_COL_1
from constants import SEISMIC3D_0
from constants import SEISMIC3D_1
from constants import SEISMIC2D_0

'''Import any test classes that you are planning on integrating with
e.g. to add in the core seismic and core horizon tests
import core_seismic_tests.py
import core_horizon_tests.py
'''


#Handles to functoins required to run tests
#GeoDataSync points to the correct impl for this client
GeoDataSync=None
#IDComaprison is required if IDs are ever compared
IDComparison=None

'''
    Insert here class or classes implemeting some tests.
    If you are making an aggregate file
    
class DummyTestCase(unittest.TestCase):

    def __init__(self,server,repo,config,methodName):
        super().__init__(methodName)
        self.server=server
        self.config=config
        self.repo=repo
        self.longMessage=False
   
    def testTryThis(self):
        
    
    def getTestSuite(server,repo,config):
       suite=unittest.TestSuite()
       
       suite.addTest(DummyTestCase(server,repo,config,"testTryThis"))
       
       return suite
 '''
            

def initModule(geodatasyncFn,idCompFn):
    '''If this is running the tests in a class(es) defined in this module
    we initialize the globals
    '''
    global GeoDataSync
    GeoDataSync=geodatasyncFn     
    global IDComparison
    IDComparison=idCompFn
    '''If we are aggregating, we need to initialse each module we are using'''
    core_seismic_tests.initModule(geodatasyncFn,idCompFn)
    core_horizon_tests.initModule(geodatasyncFn,idCompFn)
    '''We could do both but mixing is not recommened - better a test file or
    an aggregate file'''
    
def getTestSuite(server,repo,config):
    '''get the methods of the class defined in this module
    suite=DummyTestCase.getTestSuite(server, repo, config)
    
    or if aggregating do this instead
    
    suite=TestSuite()
    suite.addTests(core_seismic_tests.getTestSuite(server,repo,config))
    suite.addTests(core_horizon_tests.getTestSuite(server,repo,config))
    
    not generally recommended but we can mix ie we could include the Dummy 
    tests, and aggregate with some other modules
    
    return suite
    '''
    
if __name__=="__main__":
    '''Creates and runs a TestExecutor. This requires the module functions
    initModule and getTestSuite to be passed in.
    '''
    TestExecutor(initModule,getTestSuite).execute()
   
   