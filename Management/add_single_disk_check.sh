#! /bin/bash

# add_disk_check.sh
#
# Matt Jones <caffeinatedengineering@gmail.com>
# Created: 01.15.2013
# Last Update: 01.24.2013
#
#
# This script will add a disk check to a host configuration file.
# The input file is a list of short host names and can be generated using grep,
# for example to find servers with foo and bar in their names use grep -iE 'foo|bar' > output.
# Awk and sort can be used to further clean, organize, and filter the list.
# The script will take care of getting the correct path and configuration file.
#
# Command Examples: ./add_disk_check.sh <input file> <disk path> <threshold>
#                   ./add_disk_check.sh Host_List /var/backups 10
#




InputFile=$1 # a list of server names.
location="$2" # the path to the partition you wish to monitor
command='check_remote_disk' # the icinga command to be used, must be the same as listed in command.cfg
threshold="$3" # the threshold, should be a whole number
ServiceTemplate=$4

read -d '' service_check << EOF

define service{ 
            use                             $ServiceTemplate                    
            host_name                       default_host               
            service_description             Disk Space - $location                ; check the disk space on a partition 
            check_command                   $command!$threshold%!$location         ; <command> <critical threshold> <location> 
            }
EOF

echo "$service_check" # make sure this is what you want inserted into the config file

#while read line
#    do
#
#    set $(echo $line | awk '{print $1}') 
    host=$1 # the short host name
    server="$host.cfg" # this adds .cfg to the list for the locate command below
    cmd="locate -b \\$server" # this will match excately the file, hence adding .cfg to it from above.  Without this results will be unpredictable
    set $($cmd)
    config_file=$1 # the full path to the icinga host configuration file
    echo $server # confirm the output from the list
    echo $config_file # confirm the path and configuration file are the ones you want edited
    #echo "$service_check" >> $config_file # add the service check to the end of the configuration file
    #sed -i.bak s/default_host/$host/g $config_file # change the default_host in the check to the actual host.
    # You can skip the above command by moving the service chack variable to inside the loop and set the hostname
    # but I prefer it like this for the sake of readability
    rm -f *.bak # clean up after sed   

#done < $InputFile

