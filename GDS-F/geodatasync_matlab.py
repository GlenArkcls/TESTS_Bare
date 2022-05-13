# -*- coding: utf-8 -*-
"""
Provides an interface to the MATLAB GDS system

This file provides a 'GeoDataSync' function which is used for call to the GDS 
system via MATLAB.
This is accomplished by calling the GDSWrapper function on the MATLAB side. 
First however we need to do some translation of the input arguments. Currently 
this involves just turning instances of byte array strings into full string 
types.

After the GDS wrapper is called the return from MATLAB must again be translated.
The opposite process takes place on string types (ie strings go to byte 
arrays - ASCII strings). In addition numeric arrays come back wrapped in 
specific MATLAB types (mlarray). We want to translate these into ordinary 
Python lists. This ensures that the Python tests see exactly the same thing 
whether they are run natively (ie against Python GDS) or against MATLAB, and 
avoid potentially subtle bugs if a return from one test is used directly as
input to another (and therefore not of the type expected)

Note that the types of the mlarrays cannot be directly checked - the types are 
produced within the MATLAB libraries and have type e.g. 'mlarray.single'. 
From this module, external to that library, we see these as e.g.
'matlab.mlarray.sngle' and there is no way of accessing the internal type.
For this reason we must do the type detection by locating strings within the
object repr.

This code is currently quite generic, in particular it doesn't require 
knowledge of what actual function was called or what its inputs/outputs 
are except in one case (nested 1-D arrays - method is translateMLArray) where 
we must know a particular action must be applied which is not deducable simply
from the data structure.Anyone extending the GDS API must be awrae of this 
possibility and add any new return to the method if appropriate.

Some of the methods have been slightly generalised beyond what currently
appears (for instance, general recursion of the lists), providing hopefully a
degree of future proofing. However, much depends on whether the input/output 
conform to some particular constraints so:
    
NB future additions to the GDS API might break this code!!


Created on Wed Apr 20 14:40:30 2022

@author: lewthwju
"""

import matlab
import matlab.engine


from collections.abc import Mapping
import os.path
import pathlib

eng=None

def start():
   '''Starts the MATLAB engine
   '''
   global eng
   #start MATLAB engine (no GUI)
   eng=matlab.engine.start_matlab()
   #add the path for the GDS wrppaer code
   codepath=os.path.join (pathlib.Path(__file__).resolve().parent,"matlab")
   eng.addpath(codepath)
   #add the path to the actual code to test
   codepath=os.path.join (pathlib.Path(__file__).resolve().parent,"code")
   eng.addpath(codepath)
   

def startConnection(port=None):
    '''Starts the connection and returns the server
    '''
    if port is None:
        port=eng.getPort()
    server=eng.connect(port)
    return server



def closeConnection(server):
    '''Nothin to do for MATLAB
    '''
    pass

def translateInputList(ls):
    '''Check an input list for any byte arrays - these are translated into 
    strings
    '''
    out=[]
    for el in ls:
        if type(el) is bytes:
            out.append(bytesToString(el))
        elif type(el) is list:
            out.append(translateInputList(el))
        else:
            out.append(el)
    return out

def translateInputArgs(*args):
    '''Python GDS uses byte arrays rather than strings in many places
    - they need to be strings
    '''
    ret=[]
    for arg in args:
        if type(arg) is bytes:
            ret.append(bytesToString(arg))
        elif type(arg) is list:
            ret.append(translateInputList(arg))
        else:
            ret.append(arg)
    return ret

def isMatlabArray(obj):
     return repr(type(obj)).count("mlarray")>0

def translateOutputDict(input):
    '''Translates a dictonary fomr the MATLAB ouptu to plain Python types
    Any dictionary output will be using strings for keys
    but the python GDS system uses byte arrays - so we need to translate those.
    Any numeric arrays are returned as MATLAB types, er need to replace with orfinary
    Python lists
    Some returns are 1-D arrays of numbers that MATLAB returns as a nested list, ie
    [[1.,2.,3.,4....]]. We need to remove the outer layer and return [1.,2.,3.,4...].
    Beware that sometimes the nested list is correct - ie if asking for data from a set of traces
    and one trace only is returned this will - correctly - be a nested list
    '''
    ret={}
    for k,v in input.items():
        #matlab array types need converted to normal python lists
        if isMatlabArray(v):
            v=translateMLArray(v)
        elif type(v) is list:
            v=translateOutputList(v)
        elif type(v) is str:
            v=stringToBytes(v)
        #Unpack these arrays-currently packaged as nested lists
        if k in ["Inlines","Xlines","XCoords","YCoords","ZCoords","SurfVals","HorzVals","Values","Data"]:
            if not v is None and len(v)>0:
                v=v[0]
        #LogVals can appear in two contexts and needs this messy handling
        if k in ["LogVals"]:
            if not v is None and len(v)>0:
                if type(v[0][0]) is list:
                    v1=[]
                    for el in v:
                        if not el is None and len(el)>0:
                            v1.append(el[0])
                else:
                    v1=v[0]
                v=v1
        #Alter the key to a byte string (ie ASCII) rather than string type
        ret[stringToBytes(k)]=v
    return ret

def translateMLArray(arr):
    '''Turns a MATLAB type representing a numeric array into a normal list
    Recurses to handle nested lists
    '''
    out=[]
    if repr(type(arr)).count("single")>0:
        for el in arr:
            if isMatlabArray(el):
                out.append(translateMLArray(el))
            else:
                out.append(float(el))
    elif repr(type(arr)).count("double")>0:
        for el in arr:
            if isMatlabArray(el):
                out.append(translateMLArray(el))
            else:
                out.append(float(el))
    elif repr(type(arr)).count("int32")>0:
        for el in arr:
            if isMatlabArray(el):
                out.append(translateMLArray(el))
            else:
                out.append(int(el))
    elif repr(type(arr)).count("int64")>0:
        for el in arr:
            if isMatlabArray(el):
                out.append(translateMLArray(el))
            else:
                out.append(int(el))
    return out

def translateOutputList(ls):
    '''Changes strings to byte arrays
    Translates any matlab array found as an element
    Recurses lists, and leaves everything else untouched
    '''
    out=[]
    for el in ls:
        if type(el) is list:
             out.append(translateOutputList(el))
        elif type(el) is str:
            out.append(stringToBytes(el))
        elif isMatlabArray(el):
            out.append(translateMLArray(el))
        else:
            out.append(el)
    return out
    
def translateOutput(output):
    if isinstance(output,Mapping):
        output=translateOutputDict(output)
    elif isinstance(output,list):
        output=translateOutputList(output)
    elif isMatlabArray(output):
        output=translateMLArray(output)
    return output
    
def bytesToString(input):
    return str(input,"utf-8")

def stringToBytes(input):
    return bytes(input,"ascii")


def GeoDataSync(fn,server,*args):
    '''This method first translates the args suitable for calling
    MATLAB, then calls the wrapper within MATlAB (GDSWrapper), and then does whatever
    is required on the output from MATLAB before passing it back
    '''
    nargs=translateInputArgs(*args)
    output=eng.GDSWrapper(fn,server,*nargs,nargout=1)
    output=translateOutput(output)
    return output