#! /bin/bash

list="output.txt"

#set $(ls *.cfg)
#list=$1
ls *.cfg > $list


while read line
    do
        set $(echo $line)
        server=$1
	
	#base checks 
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/[^a-z]/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/home/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/tmp/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/usr/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/var[^\/a-z]/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_disk\n" if (/Disk Space - \/var\/log/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tclusters\n" if (/Cluster/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\t\sys_uptime\n" if (/Uptime/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tntp\n" if (/NTP Offset [^Cluster]/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tmachine_type\n" if (/Machine Type [^Cluster]/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_memory\n" if (/Memory|Swap/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_processes\n" if (/Processes/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tu_load\n" if (/Load/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tssh\n" if (/SSH/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tcron\n" if (/Cron/);' $server

	
	#app disk checks
	perl -pi -e 'print "\tservicegroups\t\t\tmonitoring_disk\n" if (/Disk Space - \/usr\/local\/icingadata/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tmonitoring_disk\n" if (/Disk Space - \/[^local]icingadata/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tmonitoring_disk\n" if (/Disk Space - \/icingadata/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tvar_export_disk\n" if (/Disk Space - \/var\/export/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tbgwdata_disk\n" if (/Disk Space - \/bgwdata/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tvar_spool_disk\n" if (/Disk Space - \/var\/spool/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tdata_disk\n" if (/Disk Space - \/data/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tmsgdata_disk\n" if (/Disk Space - \/msgdata/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tsvcs_disk\n" if (/Disk Space - \/svcs/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tu01_disk\n" if (/Disk Space - \/u01/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tbackup_disk\n" if (/Disk Space - \/backup/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\ttrovix_disk\n" if (/Disk Space - \/trovix\.com/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tsearch_disk\n" if (/Disk Space - \/search/);' $server
	
	#app service checks
	perl -pi -e 'print "\tservicegroups\t\t\rgmanager_service\n" if (/Service - rgmanager/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\dns_service\n" if (/DNS Lookup Check/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tmonitoring_service\n" if (/Git/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tamazon_service\n" if (/Amazon/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tqpidd_broker_service\n" if (/Service - qpidd_broker/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tpostgres_service\n" if (/Service - postgresql/);' $server
	perl -pi -e 'print "\tservicegroups\t\t\tmysql_service\n" if (/Service - mysql/);' $server
	

	#perl -pi -e 'print "\tservicegroups\t\t\tvar_export_disk\n" if (/Disk Space - \/var\/export/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tvar_export_disk\n" if (/Disk Space - \/var\/export/);' $server
	#perl -pi -e 'print "\tservicegroups\t\t\tvar_export_disk\n" if (/Disk Space - \/var\/export/);' $server

    done < $list
