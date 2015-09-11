#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#
#                         package-manager
#                     (c) 2015 Fabian Thüring
#
# This file is distributed under the MIT Open Source License. See 
# LICENSE.TXT for details.
#
################################################################################

import os
import uuid

def appendRandomString(baseDir, isDir):
    """ Append a random string to the base directory """ 
    if not baseDir.endswith('/'):
        baseDir += str('/')
    
    while True:
        tmpDir = str(uuid.uuid4())[:10].replace("-","")
        if isDir:
            if not os.path.isdir(baseDir + tmpDir):
                baseDir += tmpDir
                break
        else:
            if not os.path.isfile(baseDir + tmpDir):
                baseDir += tmpDir
                break
    return baseDir
