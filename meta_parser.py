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

import error
import version

import os
from time import gmtime, strftime

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class MetaFileParser:
    """ Parse the meta-file """
    def __init__(self):
        HOME = os.environ['HOME']
        
        if HOME == None:
            error.fatal("environment variable $HOME is not set")
        
        self._metaDirName  = HOME+'/.package-manager/'
        self._metaFileName = HOME+'/.package-manager/install.yml'
        
        if os.path.isdir(self._metaDirName):
            self._metaDirIsPresent = True
            
        if os.path.isfile(self._metaFileName):
            metaFile = file(self._metaFileName, 'r')
            self._installedPackages = load(metaFile, Loader=Loader)
            metaFile.close()

            if self._installedPackages is None:
                self._installedPackages = dict()

    """ Add a package from the meta-file index """
    def add(self, packageName):
        if packageName in self._installedPackages:
            raise RuntimeError
        else: 
            self._installedPackages[packageName] = 'installed'
    
    """ Remove a package from the meta-file index """
    def remove(self, packageName):
        if not packageName in self._installedPackages:
            raise RuntimeError
        else: 
            del self._installedPackages[packageName]

    """ Check if package is already installed """
    def isInstalled(self, packageName):
       return True if packageName in self._installedPackages else False
        
    """ Update meta-file """
    def commitUpdate(self):
        if not self._metaDirIsPresent:
            os.mkdir(self._metaDirName)
        
        metaFile = file(self._metaFileName, 'w')
        metaFile.write("# package-manager ("+version.__VERSION__+") - "+\
                       strftime("%a, %d %b %Y %H:%M:%S\n"))
        if bool(self._installedPackages):
            metaFile.write(dump(self._installedPackages, Dumper=Dumper, 
                           default_flow_style=False))
        metaFile.close()

    """ Private attributes """
    _metaFileName = ""
    _metaDirName  = ""
    _metaDirIsPresent = False
    _installedPackages = {}
