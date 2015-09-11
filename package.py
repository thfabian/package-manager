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
import script
import misc

import os
import sys
import tempfile
import shutil
import subprocess

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class PackageManager:
    """ Manage packages """
    def __init__(self, packageDir):
        # Set package directory
        self._packageDir = packageDir
        if not os.path.isdir(self._packageDir):
            error.fatal("package directory '%s' is invalid" % (self._packageDir))
            
        # Get information about the terminal
        row, col = os.popen('stty size', 'r').read().split()
        self._consoleWidth = int(col)
        
        self._HOME = os.environ['HOME']
        if self._HOME == None:
            error.fatal("environment variable $HOME is not set")
        
    def listAvailPackages(self):
        """ Print all available packages and exit """
        
        delimiterLen = (self._consoleWidth - len(self._packageDir) - 2)/2
        print delimiterLen*'-',self._packageDir,delimiterLen*'-'
        
        packages = []
        for f in os.listdir(self._packageDir):
            if f.endswith('.yml'):
                packages.append(f.replace('.yml',''))
        
        packages.sort()
        for p in sorted(packages, key=lambda s: s.lower()):
            print p
        
        sys.exit(0)
        
    def install(self, fileName, metaFile):
        """ Install the package given by fileName """
        
        if metaFile.isInstalled(fileName):
            print "%s is already installed" % fileName
            return
        
        packageFileName = self._packageDir + '/' + fileName + '.yml'
        packageData = self.parsePackageFile(packageFileName, fileName)
        
        self.getSudo(packageData)

        print "Installing %s" % fileName
        
        tdir = misc.appendRandomString(self._HOME, True)
        buildscript = script.BuildScript(packageData, tdir)
        
        # Setup
        self.printStatus("Cloning git")
        (err, returncode) = buildscript.invokeScriptSetup()

        if returncode != 0:
            self.printFailed()
            self.printTraceBack(err)
            error.fatal("setup script failed with return code %i" 
                        %(returncode))
        self.printSuccess()
        
        # Compile
        self.printStatus("Compiling")
        (err, returncode) = buildscript.invokeScriptCompile()

        if returncode != 0:
            self.printFailed()
            self.printTraceBack(err)
            error.fatal("compile script failed with return code %i" 
                        %(returncode))
        self.printSuccess()
        
        # Install
        self.printStatus("Installing")
        (err, returncode) = buildscript.invokeScriptInstall()

        if returncode != 0:
            self.printFailed()
            self.printTraceBack(err)
            error.fatal("install script failed with return code %i" 
                        %(returncode))
        self.printSuccess()
        
        # Cleanup
        self.printStatus("Cleaning up")
        buildscript.cleanup()
        metaFile.add(fileName)
        self.printSuccess()     

    def remove(self, fileName, metaFile):
        """ remove the package given by fileName """
        
        if not metaFile.isInstalled(fileName):
            print "%s is not installed" % fileName
            return
        
        packageFileName = self._packageDir + '/' + fileName + '.yml'
        packageData = self.parsePackageFile(packageFileName, fileName)

        self.getSudo(packageData)
        
        print "Removing %s" % fileName
        
        tdir = misc.appendRandomString(self._HOME, True)
        removescript = script.RemoveScript(packageData, tdir)
        
        # Setup
        self.printStatus("Removing")
        (err, returncode) = removescript.invokeScriptRemove()

        if returncode != 0:
            self.printFailed()
            self.printTraceBack(err)
            error.fatal("setup script failed with return code %i" 
                        %(returncode))
        self.printSuccess()
        
        # Cleanup
        self.printStatus("Cleaning up")
        removescript.cleanup()
        metaFile.remove(fileName)
        self.printSuccess() 


    def parsePackageFile(self, packageFilename, packageName):
        """ Parse the package file given as a YAML file """
        if os.path.isfile(packageFilename):
            packageFile = file(packageFilename, 'r')
            packageData = load(packageFile, Loader=Loader)
            return packageData
        else:
            error.fatal("unable to locate package %s" % packageName)
        return None

    def getSudo(self, packageData):
        """ Elevate ourselves if sudo is required """
        try:
            if packageData['sudo'] and os.getuid() != 0:
                devNULL = open(os.devnull, 'w')
                child = subprocess.Popen("sudo id", stdout=devNULL, shell=True,
                                         stderr=devNULL)
                child.wait()
                devNULL.close()
        except KeyError:
            pass

    def printStatus(self, msg):
        """ Print a status message """
        out = "-- %s ... " % msg
        self._curStatusMsgLen = len(out)
        print out,
        sys.stdout.flush()
        
    def printTraceBack(self, err):
        """ Print stack trace of the error """
        err = filter(None, err)
        if err:        
            print "Traceback (most recent call last):"
            for e in err:
                print "> %s" % e
        
    def printSuccess(self):
        pad = 30 - self._curStatusMsgLen
        print pad*' ' + '[DONE]'
        
    def printFailed(self):
        pad = 30 - self._curStatusMsgLen
        print pad*' ' + '[FAIL]'
        
    """ Private attributes """
    _packageDir = ''
    _HOME = ''
    _curStatusMsgLen = 0
    _consoleWidth = -1
