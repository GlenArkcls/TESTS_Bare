# -*- coding: utf-8 -*-
"""
Created on Fri May  6 20:18:39 2022

@author: lewthwju
"""
import sys
import argparse
import unittest
from testconfigbuilder import TestConfigBuilder



class TestExecutor:
    def __init__(self,
                 initModuleFn,
                 getTestSuiteFn):
        self.__initModule=initModuleFn
        self.__getTestSuite=getTestSuiteFn
        
        
    def execute(self):
        
        parser=argparse.ArgumentParser(description="Run GDSAutoTests")
        parser.add_argument('-c','--client', choices=['python','matlab'],default="python")
        parser.add_argument('-s','--server', choices=["petrel"],default="petrel")
        parser.add_argument('-t','--type', choices=["blank","bootstrapped","simple"],default="blank")
        parser.add_argument('-p','--port',type=int)
        parser.add_argument('-w','--wait',action="store_true",default=False)
        parser.add_argument('--trace',action="store_true",default=False)
        parser.add_argument('-v','--verbosity',type=int,default=2)
        args=parser.parse_args()
        if args.wait:
            input("Hit enter to continue.")    
        try:    
            
            #Create the configuration
            configBuilder=TestConfigBuilder(args.client,args.server,args.type,args.port)
            configBuilder.setup()
            #grab the functions and initialise the module
            geodatasyncFn,idCompFn=configBuilder.getFunctions()
            self.__initModule(geodatasyncFn,idCompFn,args.trace)
            success,server,errmsg=configBuilder.getServer()
          
            if success:
                assetRepo=configBuilder.getAssetRepo()
                config=configBuilder.getTestConfig()
                #Build the tests for this module
                suite=self.__getTestSuite(server,assetRepo,config)
                #Create a test runner and execute
                runner=unittest.TextTestRunner(verbosity=args.verbosity,stream=sys.stdout)
                result=runner.run(suite)
        
        except Exception as e:
            print("Exception:"+str(e))
       
        success,errmsg=configBuilder.releaseServer()
    
        print("Server disposal:" + errmsg)