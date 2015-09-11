#!/bin/sh
###########################################################-*- shell-script -*-#
#
#                         package-manager
#                     (c) 2015 Fabian Thüring
#
# This file is distributed under the MIT Open Source License. See 
# LICENSE.TXT for details.
#
################################################################################

# package-manager
PM_INSTALL_LOCATION=/usr/local/bin/package-manager
PM_SCRIPT_LOCATION=$(pwd)/package-manager.py

# bash completion
BC_INSTALL_LOCATION=/etc/bash_completion.d/package_manager_completion
BC_SCRIPT_LOCATION=$(pwd)/package_manager_completion

# Check if we are sudo
if [ $(id -u) != 0 ]; then
    printf "bootstrap: error: this script must be run as root\n"
    exit 1
fi

# Install
printf "%-40s" "Creating symlinks ... "
sudo ln -s -f $PM_SCRIPT_LOCATION $PM_INSTALL_LOCATION
sudo chmod +x $PM_INSTALL_LOCATION
printf "%10s\n" "[DONE]"
printf "%-40s" "Installing bash completion ... "
sudo cp $BC_SCRIPT_LOCATION $BC_INSTALL_LOCATION
printf "%10s\n" "[DONE]"
exit 0
