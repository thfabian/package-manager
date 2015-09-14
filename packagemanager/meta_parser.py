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

from packagemanager import __VERSION__
from . import error

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

    def add(self, packageName):
        """ Add a package to the meta-file index """
        if packageName in self._installedPackages:
            raise RuntimeError
        else: 
            self._installedPackages[packageName] = \
                [{'date': strftime("%d-%m-%Y %H:%M:%S")}]

    def remove(self, packageName):
        """ Remove a package from the meta-file index """
        if not packageName in self._installedPackages:
            raise RuntimeError
        else: 
            del self._installedPackages[packageName]

    def isInstalled(self, packageName):
        """ Check if package is already installed """
        return True if packageName in self._installedPackages else False
       
    def getInstallDate(self, packageName):
        """ Get the install date of the package """
        if self.isInstalled(packageName):
            return self._installedPackages[packageName][0]['date']
        else:
            return ""
        
    def commitUpdate(self):
        """ Update meta-file """
        if not self._metaDirIsPresent:
            os.mkdir(self._metaDirName)
        
        metaFile = file(self._metaFileName, 'w')
        metaFile.write("# package-manager ("+__VERSION__+") - "+\
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
