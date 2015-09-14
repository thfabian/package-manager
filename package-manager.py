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

import packagemanager as pm

import os
import sys
import optparse as op

class ExtendedOption(op.Option):
    """ 
    Extend the option class to allow --cmd arg, --cmd arg1,arg2 and --cmd=arg 
    """
    ACTIONS = op.Option.ACTIONS + ("extend",)
    STORE_ACTIONS = op.Option.STORE_ACTIONS + ("extend",)
    TYPED_ACTIONS = op.Option.TYPED_ACTIONS + ("extend",)
    ALWAYS_TYPED_ACTIONS = op.Option.ALWAYS_TYPED_ACTIONS + ("extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "extend":
            lvalue = value.split(",")
            values.ensure_value(dest, []).extend(lvalue)
        else:
            op.Option.take_action(self, action, dest, opt, value, values,parser)

def main():
    # Package directory
    packageDir = os.path.dirname(os.path.realpath(__file__))+'/packages'

    # Install error handler
    pm.ErrorHandler(os.path.basename(sys.argv[0]))

    usage = "Usage: %prog [Options]"
    vers = "package-manager "+ pm.__VERSION__
    parser = op.OptionParser(usage=usage, version=vers, 
                             option_class=ExtendedOption)
                      
    # --avail
    parser.add_option("--avail", dest = "avail", 
                      action = "store_true", default = False,
                      help = "list all available packages")
                      
    # --install
    parser.add_option("--install", dest = "install", metavar="PACKAGE", 
                      help = "install new package(s)")
   
    # --remove
    parser.add_option("--remove", dest = "remove", metavar="PACKAGE", 
                      help = "remove package(s)")
                      
    # --reinstall
    parser.add_option("--reinstall", dest = "reinstall", metavar="PACKAGE", 
                   help = "remove package if present and install package(s) again")
                   
    # --package-dir
    parser.add_option("--package-dir", dest = "package_dir", 
                      action = "store_true", default = False,
                      help = "print package directory (*.yml files)")

    (options, args) = parser.parse_args()
    
    if options.package_dir:
        print packageDir
        sys.exit(0)
    
    # Setup package manager
    pManager = pm.PackageManager(packageDir)
    
    if options.avail:
        pManager.listAvailPackages()
        
    if options.install:
        for p in options.install.split(','):
            pManager.install(p)
            
    if options.remove:
        for p in options.remove.split(','):
            pManager.remove(p)
            
    if options.reinstall:
        for p in options.reinstall.split(','):
            pManager.remove(p)
            pManager.install(p)

    pManager.commitChange()
    
if __name__ == "__main__":
    main()
