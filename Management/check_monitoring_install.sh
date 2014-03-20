#! /bin/bash

# check_monitoring_install.sh
#
# Matt Jones <caffeinatedengineering@gmail.com>
#
# Created 12.05.2013
# Last Updated 12.05.2013
#
#
# this script will make sure that all servers in the supplied list are able to communicate with NRPE.
# If the connection was successful then the remote host will return the nrpe version number.


declare InputFile=$1 # the server list

while read line 
do
set $(echo $line | awk '{print $1}')
server=$1
echo $server && /usr/local/nagios/libexec/check_nrpe -H $server 
done < $InputFile
