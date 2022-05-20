# -*- coding: utf-8 -*-
"""
This script wraps up calling PETREL with a specific workflow designed to callback to the python test system
with the given parameters.
Created on Fri May 20 09:20:28 2022

@author: lewthwju
"""

import argparse
import os
import subprocess

PETREL_PATH="Petrel.exe"
WORKFLOW="GDSAutoTest"


def inPath(filename):
    paths=os.environ["Path"].split(";")
    for path in paths:
        fpath=os.path.join(path,filename)
        if os.path.exists(fpath):
            return True
    return False

parser=argparse.ArgumentParser(description="Run GDSAutoTests")
parser.add_argument('-c','--client', choices=['python','matlab'],default="python")
parser.add_argument('-t','--type', choices=["blank","bootstrapped"],default="blank")
parser.add_argument('--file',help="Python test file to run",required=True)
parser.add_argument('--license',help="Feature ID of PETREL license",required=True)
parser.add_argument('--petrel',help="Path to the PETREL application")
parser.add_argument('--project',help="PETREL project to open")
parser.add_argument('-p','--port',type=int)
args=parser.parse_args()


if not args.petrel is None:
    PETREL_PATH=args.petrel


if not os.path.exists(PETREL_PATH):
    if not inPath(PETREL_PATH):
        print("Failed to find PETREL from given file or on path")
        exit()
        
if not os.path.exists(args.file):
    if not inPath(args.file):
        print("Failed to find test file '{}' in path".format(args.file))
        exit()

cmdstr=""
if args.port is None:
  cmdstr=str.format("{} -runWorkflow {} -sparm client={},config={},testfile={} -licensePackage {} {}",PETREL_PATH,WORKFLOW,args.client,args.type,args.file,args.license,args.project) 
else:
  cmdstr==str.format("{} -runWorkflow {} -sparm client={},config={},testfile={} -nparm port={} -licensePackage {} {}",PETREL_PATH,WORKFLOW,args.client,args.type,args.file,args.port,args.license,args.project)   

subprocess.Popen(cmdstr)
