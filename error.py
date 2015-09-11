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

from sys import exit

globalErrorHandler = None

class ErrorHandler:
    """ Global error handler """
    def __init__(self, progName):
        global globalErrorHandler
        self._progName = progName
        globalErrorHandler = self
    
    def _fatal(self, msg):
        """ Print an error message and die """
        print "%s: error: %s" % (self._progName, msg)
        exit(1)
        
    def _warning(self, msg):
        """ Print a warning message """
        print "%s: warning: %s" % (self._progName, msg)
      
    _progName = ""
    
def fatal(msg):
    """ Print an error message and die """
    global globalErrorHandler
    globalErrorHandler._fatal(msg)
    
    
def warning(msg):
    """ Print a warning message """
    global globalErrorHandler
    globalErrorHandler._warning(msg)
