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

class Preprocessor:
    """ Preprocessor for string replacement """
    def __init__(self, replacement):
        self._replacement = replacement
    
    def process(self, string):
        """ Replace strings """
        for r in self._replacement:
            string = string.replace(r, self._replacement[r])
        return string

    """ Private attributes """
    _replacement = dict()
