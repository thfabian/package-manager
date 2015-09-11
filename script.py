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
import misc

import os
import subprocess
import shutil

class Script:
    """ Script base class """
    def __init__(self, packageData, tempDir):
        self._packageData = packageData
        self._tempDir = tempDir
        
        if self._packageData is None:
            error.fatal("invalid package file")
        
        self._packageName = self.extract('name')
        if self._packageName is None:
            error.fatal("package file invalid: variable 'name' is missing")

        os.mkdir(self._tempDir)
        self._devNULL = open(os.devnull, 'w')
        
    
    def convertToFile(self, scriptString, filename):
        """ 
        Convert string to script file by adding preamble '#!/bin/sh' aswell as
        trailing '\n' and error handling code
        """
        scriptString = str("#!/bin/sh\nset -e\nset -v\n") + scriptString + \
                       str("\n")
        scriptFileName = os.path.join(str(self._tempDir), str(filename))
        with open(scriptFileName, "w") as scriptFile:
            scriptFile.write(scriptString)
        return scriptFileName
        
    def invokeScript(self, filename):
        """ Invoke the script given by filename """
        if filename is not None:
            cmd = str("sh ") + str(filename)
            child = subprocess.Popen(cmd, 
                                     cwd=self._tempDir, 
                                     shell=True, 
                                     stdout=self._devNULL, 
                                     stderr=subprocess.PIPE)
            err = child.communicate()
            if child.returncode != 0:
                self.cleanup()
            return (err, child.returncode)
        else:
            print "oops"
            return (None, 0)
        
    def extract(self, key):
        """ Extract information form packa data """
        try:
            return self._packageData[key]
        except KeyError:
            return None  
            
    def cleanup(self):
        """ Cleanup workspace """
        shutil.rmtree(self._tempDir)
        self._devNULL.close()
    
    """ Protected attributes """
    _packageData = ''
    _packageName = ''
    _tempDir = ''
    _devNull = None
        
class BuildScript(Script):
    """ Convert information form package file into executable scripts """
    def __init__(self, packageData, tempDir):
        Script.__init__(self, packageData, tempDir)
        self.buildSetupScript()
        self.buildCompileScript()
        self.buildInstallScript()

    def buildSetupScript(self):
        """ 
        Build the setup script which either copies the data or invokes git to
        clone a repository
        """ 
        path = self.extract('path')
        git = self.extract('git')

        if git != None and path != None:
            error.fatal("package file invalid: 'path' and 'git' are mutually "\
                        "exclusive")
        
        script = ""
        dest = os.path.join(str(self._tempDir), str(self._packageName))
        if path:
            if not os.path.isdir(path):
                error.fatal("package file invalid: variable 'path' does not"\
                            " exist")
            script += str("cp -r ") + str(path) + str(" ") + str(dest)
        elif git:
            script += str("git clone '") + str(git) + str("' ") + str(dest)
        else:
            error.fatal("package file invalid: neither 'path' nor 'git' are"\
                        " provided")
        
        self._tempDirAfterSetup = dest
        self._script_setup = self.convertToFile(script, "setup.sh")

    def buildCompileScript(self):
        """ 
        Build the compile script which puts together the entries of 'compile'
        """ 
        compileData = self.extract('compile')

        if compileData is not None:
            script = ""
            
            # We automatically change in the copied directory
            script += str("cd ") + self._tempDirAfterSetup + str("\n")
            
            for cmd in compileData:
                script += str(cmd) + str("\n")

            self._script_compile = self.convertToFile(script, "compile.sh")
        
    def buildInstallScript(self):
        """ 
        Build the install script which puts together the entries of 'install'
        """ 
        installData = self.extract('install')

        if installData is not None:
            script = ""
            
            # We automatically change in the copied directory
            script += str("cd ") + self._tempDirAfterSetup + str("\n")
            
            for cmd in installData:
                script += str(cmd) + str("\n")

            self._script_install = self.convertToFile(script, "install.sh")
            
    def invokeScriptSetup(self):
        """ Invoke the setup script and report error's """
        return self.invokeScript(self._script_setup)
        
    def invokeScriptCompile(self):
        """ Invoke the compile script and report error's """
        return self.invokeScript(self._script_compile)
        
    def invokeScriptInstall(self):
        """ Invoke the install script and report error's """
        return self.invokeScript(self._script_install)
        
    """ Private attributes """
    _tempDirAfterSetup = ''
    _script_setup = None
    _script_compile = None
    _script_install = None
    
class RemoveScript(Script):
    def __init__(self, packageData, tempDir):
        Script.__init__(self, packageData, tempDir)
        self.buildRemoveScript()
        
    def buildRemoveScript(self):
        """ 
        Build the remove script which puts together the entries of 'remove'
        """ 
        removeData = self.extract('remove')

        if removeData is not None:
            script = ""
            for cmd in removeData:
                script += str(cmd) + str("\n")

            self._script_remove = self.convertToFile(script, "remove.sh")
            
    def invokeScriptRemove(self):
        """ Invoke the remove script and report error's """
        return self.invokeScript(self._script_remove) 
    
    """ Private attributes """
    _script_remove = None
