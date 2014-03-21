To install the scripts clone the repo to your system and place the files in either your nagios or icinga executable directories, most commonly this is /usr/local/nagios/libexec.  You could run them from any location you want with few issues.  For icinga use the following steps:

1. Add the location of the icinga_plugins directoty to /etc/icinga/resource.cfg as a new USER variable
2. Add the plugin command to /etc/icinga/conf.d/commands.cfg
3. If necessary add the full path/to/plugin command to /etc/nagios/nrpe.cfg 

Each script has a sample command that can be used as a guideline for either nrpe or icinga.  You may need to adjust some parameters but you should be able to get it working by comparing the commands in the script with local examples currently running on your system.  For further examples check out the icinga [commands.cfg documentation](http://docs.icinga.org/latest/en/sample-commands.html) and the [nrpe.cfg documentation](http://nagios.sourceforge.net/docs/nrpe/NRPE.pdf)
