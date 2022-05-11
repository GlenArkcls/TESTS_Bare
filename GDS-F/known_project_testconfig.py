# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:38:56 2022

@author: lewthwju
"""

import test_config
from test_utils import *

SEISMIC_COLLECTION_ID=[b'F3_Demo (OpendTect)',b'://1d9a2dd1-dd1d-4676-a92e-6057e64d33c2/2b200fd7-92b4-4f8f-9a0a-cc6d15dcc5f3']
SEISMIC_ID=[b'All lines',b'://1d9a2dd1-dd1d-4676-a92e-6057e64d33c2/b3be49d9-d5b7-4869-b21d-c35c015e62fb']
SURFACE_ID=[b"Adrian's Surface",b'://1d9a2dd1-dd1d-4676-a92e-6057e64d33c2/dcde600f-5a61-4b12-90e4-15b2514dbbf2']

SEISMIC_LIST=[[b'All lines',
  b'://1d9a2dd1-dd1d-4676-a92e-6057e64d33c2/b3be49d9-d5b7-4869-b21d-c35c015e62fb'],
 [b'Coloured-AI',
  b'://1d9a2dd1-dd1d-4676-a92e-6057e64d33c2/a0a9b34f-5333-4c65-834b-7104a4ec78ce']]

class KnownProjectTestConfig(test_config.TestConfig):
    def __init__(self):
        self.seismicCollectionID=SEISMIC_COLLECTION_ID
        self.seismic3DID=SEISMIC_ID
        self.surfaceID=SURFACE_ID
     