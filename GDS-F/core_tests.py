# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:20:35 2022

@author: lewthwju
"""
import os
import sys


file_dir=os.path.dirname(__file__)
sys.path.append(file_dir)


import unittest
from executor import TestExecutor


import core_seismic_tests
import core_surface_tests
import core_project_tests
import core_horizon_tests
import core_pointset_tests
import core_well_tests
import core_fault_tests
import core_wavelet_tests
import core_polygon_tests



def initModule(geodatasyncFn,idCompFn,trace):
    core_seismic_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_surface_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_project_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_horizon_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_pointset_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_well_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_fault_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_wavelet_tests.initModule(geodatasyncFn, idCompFn,trace)
    core_polygon_tests.initModule(geodatasyncFn, idCompFn,trace)

def getTestSuite(server,repo,config):
    suite=unittest.TestSuite()
    suite.addTests(core_project_tests.getTestSuite(server,repo,config))
    suite.addTests(core_seismic_tests.getTestSuite(server,repo,config))
    suite.addTests(core_surface_tests.getTestSuite(server,repo,config))
    suite.addTests(core_horizon_tests.getTestSuite(server,repo,config))
    suite.addTests(core_pointset_tests.getTestSuite(server,repo,config))
    suite.addTests(core_well_tests.getTestSuite(server,repo,config))
    suite.addTests(core_fault_tests.getTestSuite(server,repo,config))
    suite.addTests(core_wavelet_tests.getTestSuite(server,repo,config))
    suite.addTests(core_polygon_tests.getTestSuite(server,repo,config))
    return suite


    
    
if __name__=="__main__":
    TestExecutor(initModule,getTestSuite).execute()
   
    

            