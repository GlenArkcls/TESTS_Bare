# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:33:23 2022

This is a base class for the Test configurations.

It exists primarily to document the functions that need implemented for various tests.

The NotImplementedError is thrown to show a user that a needed method has not been implemneted in a subclass
and will lead to the test system reporting an 'error' rather than passing or failing the tested function 

There are also implemented some utility functions that pass derived values - these should not be reimplemented

@author: lewthwju
"""


from abc import ABC,abstractmethod
        

class TestConfig(ABC):
    
    '''
    3D Seismic - provide the geometry and data for creating/verifying a 3D seismic volume
    '''
    @abstractmethod
    def get3DSeismicGeometry(self,name=None):
        pass 
    def get3DSeismicData(self,name=None):
         raise NotImplementedError
#    '''
#    Derive the list of inlines from the geometry and return that list
#    '''
#    def get3DGeometryInlines(self):
#        minIL=self.get3DSeismicGeometry()[b"MinInline"]
#        maxIL=self.get3DSeismicGeometry()[b"MaxInline"]
#        incIL=self.get3DSeismicGeometry()[b"InlineInc"]
#        return [x for x in range(minIL,maxIL+1,incIL)]
#    '''
#    Derive the list of crosslines from the geometry and return that list
#    '''
#    def get3DGeometryCrosslines(self):
#        minXL=self.get3DSeismicGeometry()[b"MinXline"]
#        maxXL=self.get3DSeismicGeometry()[b"MaxXline"]
#        incXL=self.get3DSeismicGeometry()[b"XlineInc"]
#        return [x for x in range(minXL,maxXL+1,incXL)]
#    '''
#    Derive lists of inlines and crosslines from the geometry so that every pair
#    of IL,XL is represented (XL fastest)
#    '''
#    def get3DGeometryILXLPairs(self):
#        ilines=self.get3DGeometryInlines()
#        xlines=self.get3DGeometryCrosslines()
#        ils=[y for z in [[x]*len(xlines) for x in ilines] for y in z] #eacxh value of ilines repeated len(xlines) times then concat
#        xls=xlines*len(ilines) #just the list of xlines repeated len(ilines) times
#        return ils,xls
    
    '''
    2D Seismic geometry and data for creating/verifying a 2D seismic line
    '''
    def get2DSeismicGeometry(self,name=None):
        raise NotImplementedError
    def get2DLineData(self,name=None):
         raise NotImplementedError 
      
    '''
    Surface, geometry and data for creating/verifying a test surface
    '''
    def getSurfGeometry(self,name=None):
        raise NotImplementedError
    def getSurfVals(self):
        raise NotImplementedError  
   
    

      
        
        
        