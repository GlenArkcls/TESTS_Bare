# -*- coding: utf-8 -*-
"""
TestConfigBuilder sets up the client and server types
and also the data configuration type

It should be constructed with the names of the client,server and test configuration types,
then have 'setup' called. After that the using code can call getFunctions,getAssetRepo,getServer
and getTestConfig to initialize and run the tests.
Created on Fri Apr 29 09:26:51 2022

@author: lewthwju
"""

import asset_repo
import test_utils
from functools import partial

CLIENT_VERSION="2.2.0.0"
SERVER_VERSION="2.2.0.0"


class TestConfigBuilder:
    def __init__(self,client,server,config,port):
        self.__clientType=client
        self.__serverType=server
        self.__configType=config
        self.__port=port
        self.__server=None
        
    def __setupMatlab(self):
        import geodatasync_matlab
        self.__startTheConnection=partial(lambda port:geodatasync_matlab.startConnection(port),port=self.__port)
        self.__closeTheConnection=lambda a :a
        self.__geodatasyncFn= geodatasync_matlab.GeoDataSync
        geodatasync_matlab.start()

    def __setupPython(self):
        import geodatasync.geodatasync
        if self.__port is None:
            self.__startTheConnection=geodatasync.geodatasync.startConnection
        else:
            self.__startTheConnection=partial(lambda port:geodatasync.geodatasync.openConnection(port),port=self.__port)
        self.__closeTheConnection=geodatasync.geodatasync.closeConnection
        self.__geodatasyncFn= geodatasync.geodatasync.GeoDataSync   
            
           
    def __setupPetrel(self):
        import geodatasync_petrel
        self.__idComparisonFn=geodatasync_petrel.IDComparison
        geodatasync_petrel.startPetrel(self.__port)
            
    def setup(self):
        systemInfo={"clientVersion":CLIENT_VERSION,
                    "serverVersion":SERVER_VERSION}
        self.__assetRepo=asset_repo.AssetRepository()    
        if self.__clientType=="matlab":
                self.__setupMatlab()
        elif self.__clientType=="python":
                self.__setupPython()
                
        if self.__serverType=="petrel":
                self.__setupPetrel()
                systemInfo["systemType"]="PET"
        asset_repo.initModule(self.__geodatasyncFn)
        test_utils.initModule(self.__geodatasyncFn)
        if self.__configType=="blank":
            import blank_project_testconfig
            self.__testConfig=blank_project_testconfig.BlankProjectTestConfig(systemInfo)
        elif self.__configType=="big":
            import big_project_testconfig
            self.__testConfig=big_project_testconfig.BigProjectTestConfig(systemInfo)
        elif self.__configType=="bootstrapped":
            import bootstrapped_testconfig
            self.__testConfig=bootstrapped_testconfig.BootstrappedTestConfig(systemInfo)
            bootstrapped_testconfig.initModule(self.__geodatasyncFn)
        elif self.__configType=="simple":
            import simple_testconfig
            self.__testConfig=simple_testconfig.SimpleTestConfig(systemInfo)
            
           
    def getFunctions(self):
        return self.__geodatasyncFn,self.__idComparisonFn
        
    def getAssetRepo(self):
        return self.__assetRepo
        
    def getTestConfig(self):
        return self.__testConfig

    def getServer(self):
        try:
            self.__server=self.__startTheConnection()
            self.__assetRepo.initServer(self.__server)
            self.__testConfig.initialise(self.__server,self.__assetRepo)
            self.__geodatasyncFn("hideErrorMessages",self.__server,2)
        except Exception as e:
            print("getServer EXCEPTION "+str(e))
            return False,self.__server,"Failed" + str(e)
        return True,self.__server,"Success"

    def releaseServer(self):
        try:
            self.__closeTheConnection(self.__server)
        except Exception as e:
            return False,"Failed close:"+str(e)
        return True,"Success"


    