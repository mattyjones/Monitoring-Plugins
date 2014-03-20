#! /bin/bash

# add_server_list.sh
#
# Matt Jones <caffeinatedengineering@gmail.com>
#
# Created 12.05.2013
# Last Updated 12.05.2013
#
# This script will take a tab seperated file in the format of <server name>  <ip address>. It will create 
# a new basline configuration from a already present host by copying an already present host and then 
# changing the ip and hostname in the new file.  Sed assumes preset values in the template file so you 
# may need to adjust the commands on lines 31 and 32.
#
# Command Examples: ./add_server_list.sh <input file>> <template>
#                   ./add_server_list.sh new_servers mail_server_template.cfg
#


declare InputFile=$1
declare TemplateFile=$2

while read line
do
set $(echo $line | awk '{print $2}')
server=$1
set $(echo $line | awk '{print $1}')
ip=$1

cp $TemplateFile $server.cfg
sed -i.bak s/default_host/$server/g $server.cfg
sed -i.bak s/0.0.0.0/$ip/g $server.cfg
done < $InputFile

rm -f *.bak
