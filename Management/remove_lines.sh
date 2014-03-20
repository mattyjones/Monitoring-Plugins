#! /bin/bash

while read line
    do
        #set $(echo $line | awk '{print $1}')
        #server=$1
        #echo $line
        #echo $server

        cat $line | head -n -6 > $line.bak
        echo '' >> $line.bak
        mv $line.bak $line 
done < $1

