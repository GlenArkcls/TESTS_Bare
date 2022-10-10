# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 23:28:51 2022

SeismicGeometry wraps the GDS geometry dictionary into a class
that provides various methods on that, e.g. providing a list of crosslines.

Ideally, eventually this class will do the coordinate transform as well

@author: lewthwju
"""

import types
from functools import partial


'''
Hopefully a sufficiently irregular geomerty - actually its theta is 88 degress, probably make it more
rotated - used for testing this class only
'''
DefaultSeisGeometry={
        b'MinInline': 200,
        b'MaxInline': 218,
        b'InlineInc': 2,
        b'MinXline': 400,
        b'MaxXline': 427,
        b'XlineInc': 3,
        b'X0': 608271.29,
        b'Y0': 6076131.66,
        b'X1': 608406.363659533,
        b'Y1': 6076218.128075472,
        b'X2': 608264.37,
        b'Y2': 6076377.14,
        b'MinZ': 0.004,
        b'MaxZ': 1.848,
        b'ZInc': 0.004,
        b'InlineSep': 23.687,
        b'XlineSep': 27.2863908,
        b'isDepth': 0
        }
        
'''
Hopefully a sufficiently irregular geomerty - actually its theta is 88 degress, probably make it more
rotated - used for testing this class only
'''
BasicSeisGeometry={
        b'MinInline': 0,
        b'MaxInline': 1,
        b'InlineInc': 1,
        b'MinXline': 0,
        b'MaxXline': 1,
        b'XlineInc': 1,
        b'X0': 0,
        b'Y0': 0,
        b'X1': 1,
        b'Y1': 1,
        b'X2': 0,
        b'Y2': 1,
        b'MinZ': 0.004,
        b'MaxZ': 1.848,
        b'ZInc': 0.004,
        b'InlineSep': 1,
        b'XlineSep': 1,
        b'isDepth': 0
        }

    
class SeismicGeometry:
    '''
    Initialize with a GDS geometry
    '''
    def __init__(self,GDSGeom):
        self.gdsGeom=GDSGeom
        '''
        For all the keys XXX add a
        getXXX function
        '''
        for k in self.gdsGeom.keys():
            kname=str(k,"utf-8")
            mname="get"+kname[0].upper()+kname[1:]
            mt=types.MethodType(partial(lambda self,j:self.gdsGeom[j],j=k),self)
            setattr(self,mname,mt)
        self.ilxlOrigin=[GDSGeom[b'MinInline'],GDSGeom[b'MinXline']]
        self.utmOrigin=[GDSGeom[b'X0'],GDSGeom[b'Y0']]
        c0=[GDSGeom[b'X0'],GDSGeom[b'Y0']]
        c1=[GDSGeom[b'X1'],GDSGeom[b'Y1']]
        c2=[GDSGeom[b'X2'],GDSGeom[b'Y2']]
        xlines=GDSGeom[b'MaxXline']-GDSGeom[b'MinXline']
        ilines=GDSGeom[b'MaxInline']-GDSGeom[b'MinInline']
        dXL=[(c2[0]-c0[0])/xlines,(c2[1]-c0[1])/xlines]
        dIL=[(c1[0]-c2[0])/ilines,(c1[1]-c2[1])/ilines]
        self.a00=dIL[0]
        self.a01=dXL[0]
        self.a10=dIL[1]
        self.a11=dXL[1]

        
    
    '''
    Expose the inner dictionary
    '''
    def __getitem__(self,key):
        return self.gdsGeom[key]
    def keys(self):
        return self.gdsGeom.keys()
    def values(self):
        return self.gdsGeom().values()
    
    def getInlineRange(self):
        return range(self.getMinInline(),self.getMaxInline()+1,self.getInlineInc())
    
    def getCrosslineRange(self):
        return range(self.getMinXline(),self.getMaxXline()+1,self.getXlineInc())
   
    def gridPtInCube(self,il,xl):
        return il>=self.getMinInline() and il<=self.getMaxInline() and xl>=self.getMinXline() and xl<=self.getMaxXline()
    
    def getInlineList(self):
        '''
        Derive the inline list from the geometry and return it
        '''
        minIL=self[b"MinInline"]
        maxIL=self[b"MaxInline"]
        incIL=self[b"InlineInc"]
        return [x for x in range(minIL,maxIL+1,incIL)]
    
    def getCrosslineList(self):
        '''
        Derive the list of crosslines from the geometry and return that list
        '''
        minXL=self[b"MinXline"]
        maxXL=self[b"MaxXline"]
        incXL=self[b"XlineInc"]
        return [x for x in range(minXL,maxXL+1,incXL)]
    '''
    Derive lists of inlines and crosslines from the geometry so that every pair
    of IL,XL is represented (XL fastest)
    '''
    def get3DGeometryILXLPairs(self):
        ilines=self.getInlineList()
        xlines=self.getCrosslineList()
        ils=[y for z in [[x]*len(xlines) for x in ilines] for y in z] #eacxh value of ilines repeated len(xlines) times then concat
        xls=xlines*len(ilines) #just the list of xlines repeated len(ilines) times
        return ils,xls 
    
    def getGDSGeom(self):
        return self.gdsGeom
    
    def transformUTMVector(self,utmVector):
        """Transform a UTM coord into a grid coord"""
        cx=utmVector[0]
        cy=utmVector[1]
        one_over_det=1.0/(self.a00*self.a11-self.a01*self.a10)
        xl=(self.a00*cy-self.a10*cx)*one_over_det
        il=(-self.a01*cy+self.a11*cx)*one_over_det
        return [il,xl]
    def transformUTM(self,utmCoord):
        """Transform a UTM coord into a grid coord"""
        cx=utmCoord[0]-self.utmOrigin[0]
        cy=utmCoord[1]-self.utmOrigin[1]
        one_over_det=1.0/(self.a00*self.a11-self.a01*self.a10)
        xl=(self.a00*cy-self.a10*cx)*one_over_det
        il=(-self.a01*cy+self.a11*cx)*one_over_det
        
        return [il+self.ilxlOrigin[0],xl+self.ilxlOrigin[1]]
    def transformILXLVector(self,gridVector):
        """Transforms a GridCoord into UTM coord"""
        il0=gridVector[0]
        xl0=gridVector[1]
        x=(self.a00*il0+self.a01*xl0)
        y=(self.a10*il0+self.a11*xl0)
        return [x,y]
    def transformILXL(self,gridCoord):
        """Transforms a GridCoord into UTM coord"""
        il0=gridCoord[0]-self.ilxlOrigin[0]
        xl0=gridCoord[1]-self.ilxlOrigin[1]
        x=(self.a00*il0+self.a01*xl0)
        y=(self.a10*il0+self.a11*xl0)
        return [x+self.utmOrigin[0],y+self.utmOrigin[1]]
    
   
if __name__=="__main__":
    sg=SeismicGeometry(BasicSeisGeometry)
   
    ilxl=[1.,1.]
    c0=sg.transformILXL(ilxl)
    print(str(ilxl)+"->"+str(c0))
    c1=[2,2]
    ilxl=[2,2]
    c0=sg.transformILXL(ilxl)
    print(str(ilxl)+"->"+str(c0))
    ilxl1=sg.transformUTM(c0)
   
    print(str(c0)+"->"+str(ilxl1))
    
    cvec=sg.transformILXLVector([5.,0.])
    print(cvec)
    cvec=sg.transformILXLVector([0.,5.])
    print(cvec)
    
	
    
    