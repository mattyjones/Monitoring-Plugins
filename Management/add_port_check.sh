#! /bin/bash

# add_port_check.sh
#
# Matt Jones <caffeinatedengineering@gmail.com>
# Created: 01.15.2013
# Last Update: 01.24.2013
#
#
# This script will add a new port check to a configuration file.
# The input file is a list of short host names and can be generated using grep,
# for example to find servers with foo and bar in their names use grep -iE 'foo|bar' > output.
# Awk and sort can be used to further clean, organize, and filter the list.
# The script will take care of getting the correct path and configuration file.
#
# This script may need to be modified if you do not use my python script to check the ports.
#
# Command Examples: ./add_port_check.sh <input file> <port>
#                   ./add_port_check.sh Mail_Servers 8080
#




InputFile=$1  # a list of server names.
port="$2" # the port to connect to
command='check_port'  # the icinga command to be used, must be the same as listed in command.cfg

read -d '' service_check << EOF

define service{ 
            use                             local-service                    
            host_name                       default_host               
            service_description             Service - $port        ; check the status of a given service 
            check_command                   $command!\$HOSTADDRESS\$!$port         ; <command> <service> 
            }
EOF

echo "$service_check"

while read line
    do

    set $(echo $line | awk '{print $1}') 
    host=$1 # the short host name
    server="$host.cfg" # this adds .cfg to the list for the locate command below
    cmd="locate -b \\$server" # this will match excately the file, hence adding .cfg to it from above.  Without this results will be unpredictable
    set $($cmd)
    config_file=$1 # the full path to the icinga host configuration file
    #echo $server # confirm the output from the list
    #echo $config_file # confirm the path and configuration file are the ones you want edited
    echo "$service_check" >> $config_file # add the service check to the end of the configuration file
    sed -i.bak s/default_host/$host/g $config_file # change the default_host in the check to the actual host.
    # You can skip the above command by moving the service chack variable to inside the loop and set the hostname
    # but I prefer it like this for the sake of readability
    rm -f *.bak # clean up after sed  


done < $InputFile

