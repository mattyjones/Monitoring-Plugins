#! /bin/bash

# add_host_group.sh
#
# Matt Jones <caffeinatedengineering@gmail.com>
# Created: 01.15.2013
# Last Update: 01.21.2013
#
#
# This script will take a list of servers and add them to the hostgroup with the name matching the 
# inputfile.  It searches for the 'hostgroups' directive and appends additonal groups to what is already present.
# If necessary you could also use the HostGroup var to declare an additional or seperate seperate name.  
# Uncomment it on line 16 and then add it to the sed statement on line 38. The input file is a list of short host names
# and can be generated using grep, for example to find servers with foo and bar in their names use grep -iE 'foo|bar' > output.
# Awk and sort can be used to further clean, organize, and filter the list.
#
# Command Examples: ./add_host_group.sh <input file>
#                   ./add_host_group.sh Mail_Servers
#

declare InputFile=$1
#declare HostGroup=$2



while read line 
do
set $(echo $line | awk '{print $1}')
server="$1.cfg" # this adds .cfg to the list for the locate command below
cmd="locate -b \\$server" # this will match excately the file, hence adding .cfg to it from above.  Without this results will be unpredictable
set $($cmd)
config_file=$1
set $(echo $line | grep hostgroups $config_file | awk '{print $2}')
group=$1
#echo $server #check to make sure all the values are correct before inserting into the file
#echo $group
#echo $InputFile

#if [[ $InputFile == $group ]]
if [[ $group =~ $InputFile ]] # make sure the host group is not already listed
    then
       echo "$server was already a member of that group"
    else
       sed -i.bak 5s/$group/$group,$InputFile/ $config_file
       echo "added the group $group to $server"
fi

# This is just a test line that will print important info to stdout.  It should be run on large groups to verify everything is at it should be
#echo "The server is $server, the path to the config file is $config_file, and the current hostgroup is $group, and the new group will be $group,$InputFile."

done < $InputFile
