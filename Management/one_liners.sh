#! /bin/bash

InputFile=$1


#-----------------------------------------#
#
# functions
#
#
#-----------------------------------------#


# remove a service check based upon its location in the file
function remove_service_check_by_line_number()
{
    for file in $(ls *.cfg)
        do
            sed -i.bak '132,137d' $file
    done
}

# remove a service check from a group of files
function remove_service_check_by_file()
{
    while read line
        do
           sed -i .bak '132,137d' $line
    done < $InputFile
}

function check_line_output()
{
    for file in $(ls *.cfg)
        do
            echo $file
            #sed -n '101p' $file | grep -v 'NTP Offset'
            #sed -n '115p' $file | grep -v monitoring-service
            #sed -n '80p' $file | grep -v hardware-service
	    #sed -n '87p' $file | grep -v hardware-service
	    #sed -n '94p' $file | grep -v hardware-service
 	    #sed -n '115p' $file | grep -v monitoring-service
 	    #sed -n '121p' $file | grep -Ev 'trovix-service|affanity-service'
 	    #sed -n '127p' $file | grep -v trovix-service

    done
}

function get_ip()
{
    while read line
        do
            ping -c 2 $line
    done < $InputFile
}


function update_icinga()
{
    while read line
        do
            ssh -l svcicinga $line < ./icinga_auto_update.pl /usr/bin/perl
    
    done < $InputFile
}


#--------------------------------------------#
#
# sed - search and replace
#
#--------------------------------------------#

#sed -i.bak 's/check_remote_procs!250!400!RSZDT/check_remote_procs!1024!1200!RSZDT/g' *
#sed -i.bak s/HOSTADDRESS/HOSTNAME/g *
#sed -i.bak 's/check_ssh!\$HOSTNAME\$!8080/check_ssh!\$HOSTNAME\$/g' *
#sed -i.bak 's/check_port/check_url/g' *
#sed -i.bak 's/Service - powerjobsearch/URL - :8080\/powerjobsearch/g' *
#sed -i.bak 's/Service - powerresumesearch/URL - :8080\/powerresumesearch/g' *
#sed -i.bak 's/Service - powercoursesearch/URL - :8080\/powercoursesearch/g' *
#sed -i.bak 's/Service - root/URL - :8080\//g' *
#sed -i.bak 's/Service - sourcebox/URL - :8080\/sourcebox/g' *
#sed -i.bak 's/Service - rpwclient/URL - :8080\/rpwclient/g' *
#sed -i.bak 's/local-service/base-service/g' *
#sed -i.bak '80s/base-service/hardware-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '101s/unix-service/unix-cluster-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '115s/monitoring-service/monitoring-cluster-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '87s/base-service/hardware-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '94s/base-service/hardware-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '115s/base-service/monitoring-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '121s/base-service/trovix-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak '127s/base-service/trovix-service/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak 's/check_machine_type/check_machine_type\!\$HOSTNAME\$/g' * # Very useful when adding new hostgroups to already existing configurationsh 
#sed -i.bak 's/Base - //g' *
#sed -i.bak 's/base-service/unix-service/g' * 
#sed -i.bak 's/check_remote_mem_used/check_mem_used/g' *
#sed -i.bak 's/check_remote_disk/check_disk/g' *
#sed -i.bak 's/check_remote_ntp/check_ntp/g' * 
#sed -i.bak 's/check_remote_procs/check_procs/g' *
#sed -i.bak 's/check_remote_sys_uptime/check_sys_uptime/g' *
#sed -i.bak 's/check_remote_service/check_service/g' *
sed -i.bak 's/check_remote_load/check_load/g' *
#--------------------------------------------#
#
# grep - pattern matching
#
# useful for creating input files based upon
# a host configuration file name
#
#--------------------------------------------#


# Use this command to search for application specific servers and dump them to a list
#grep -iE '<pattern>' <file> | awk -F<seperastor> '{print $2}' | sort > <output_file>
#grep -iE 'lcupd|clcupd|dllcupd' trovix_list | awk -F. '{print $2}' | sort >> Trovix_LCUPD


#-------------------------------------------#
#
# various - file utils
#
# commands that perform random tasks with 
# files
#
#-------------------------------------------#

# locate a file whoose name match excately the pattern
# Very useful when multiple files match a base name.  If used in a script pay attention to escaping
#locate -b '\<pattern>\'
#locate -b '\rse\'


#-------------------------------------------#
#
# function calls
#
#
#-------------------------------------------#

#remove_service_check_by_line_number #132 137
#remove_service_check_by_file
#get_ip
#check_line_output
#update_icinga

#-------------------------------------------#
#
# cleanup
#
#
#-------------------------------------------#

rm -rf *.bak
