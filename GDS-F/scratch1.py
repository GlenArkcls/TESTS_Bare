# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:25:06 2022

@author: lewthwju
"""

import clr
import sys
sys.path.append("C:\Program Files\Schlumberger\Petrel 2021\Public")

clr.AddReference("Slb.Ocean.Core")
clr.AddReference("Slb.Ocean.Petrel")
clr.AddReference("Slb.Ocean.Basics")

import Slb.Ocean.Core
import Slb.Ocean.Petrel
#from Slb.Ocean.Petrel.Core.Impl import *

from Slb.Ocean.Petrel import PetrelSystem
from Slb.Ocean.Core import SystemFactory

print(dir(Slb.Ocean.Core))
print(dir(Slb.Ocean.Petrel))
#print(dir(Slb.Ocean.Basics))

ps=PetrelSystem
print(dir(ps))

print(dir(SystemFactory))
