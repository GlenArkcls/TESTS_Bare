# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:11:38 2022
This class deals with a surface geometry, primarily to give the 
UTM coords from the i,j node coordinates
@author: lewthwju
"""



import types
from functools import partial
import math


TestSurfaceGeometry={
        b'SizeI': 7,
        b'SizeJ': 9,
        b'SpacingI': 23.0,
        b'SpacingJ': 13.0,
        b'OriginX': 608271.0,
        b'OriginY': 6076131.0,
        b'Theta': -20.0,
        b'isDepth': 0
        }

class SurfaceGeometry:
    '''
    Initialize with a GDS geometry
    '''
    def __init__(self,surfGeom):
        self.surfGeom=surfGeom
        '''
        For all the keys XXX add a
        getXXX function
        '''
        for k in self.surfGeom.keys():
            kname=str(k,"utf-8")
            mname="get"+kname[0].upper()+kname[1:]
            mt=types.MethodType(partial(lambda self,j:self.surfGeom[j],j=k),self)
            setattr(self,mname,mt)
        
        self.utmOrigin=[surfGeom[b'OriginX'],surfGeom[b'OriginY']]
        self.theta=surfGeom[b'Theta']
        
        
        self.a00=math.cos(self.toRadians(self.theta))*self.getSpacingI()
        self.a01=-math.sin(self.toRadians(self.theta))*self.getSpacingJ()
        self.a10=math.sin(self.toRadians(self.theta))*self.getSpacingI()
        self.a11=math.cos(self.toRadians(self.theta))*self.getSpacingJ()
        
    def toRadians(self,deg):
        return deg/180.0*math.pi
    def transformUTMVector(self,utmVector):
        """Transform a UTM coord into a grid coord"""
        cx=utmVector[0]
        cy=utmVector[1]
        one_over_det=1.0/(self.a00*self.a11-self.a01*self.a10)
        j=(self.a00*cy-self.a10*cx)*one_over_det
        i=(-self.a01*cy+self.a11*cx)*one_over_det
        return [i,j]
    def transformUTM(self,utmCoord):
        """Transform a UTM coord into a grid coord"""
        cx=utmCoord[0]-self.utmOrigin[0]
        cy=utmCoord[1]-self.utmOrigin[1]
        one_over_det=1.0/(self.a00*self.a11-self.a01*self.a10)
        j=(self.a00*cy-self.a10*cx)*one_over_det
        i=(-self.a01*cy+self.a11*cx)*one_over_det
        return [i,j]
    def transformGridVector(self,gridVector):
        """Transforms a GridCoord into UTM coord"""
        i0=gridVector[0]
        j0=gridVector[1]
        x=(self.a00*i0+self.a01*j0)
        y=(self.a10*i0+self.a11*j0)
        return [x,y]
    def transformGridCoord(self,gridCoord):
        """Transforms a GridCoord into UTM coord"""
        i0=gridCoord[0]
        j0=gridCoord[1]
        x=(self.a00*i0+self.a01*j0)
        y=(self.a10*i0+self.a11*j0)
        return [x+self.utmOrigin[0],y+self.utmOrigin[1]]
    
    
if __name__=="__main__":
    g=SurfaceGeometry(TestSurfaceGeometry)
    utm=[608284.33,6076167.64]
    gc=g.transformUTM(utm)
    print(gc)
    utm=g.transformGridCoord([0,3])
    print(utm)
    gc=g.transformUTM(utm)
    print(gc)