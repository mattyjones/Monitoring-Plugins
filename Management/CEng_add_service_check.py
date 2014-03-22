#! /usr/bin/env python

'''

 CEng_add_service_check.py

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.19.14
 Last Update 03.21.14

 Notes:  This will add a new service check to a host configuration file

 Usage:

 Command Line 1:  ./CEng_add_service_check.py

 Local Example:  ./CEng_add_service_check.py

'''

from string import Template
import sys

def main():

  # Need to use argparse to set these properly
  InheritanceTemplate = sys.argv[1]
  MonitoredInstance = sys.argv[2]
  ServiceDescription = sys.argv[3]
  ServiceCommand = sys.argv[4]
  CommandArguement1 = sys.argv[5]
  CommandArguement2 = sys.argv[6]
  HostConfigList =  = sys.argv[7]

  # a very basic service definition, a better one with all available optitions needs to be created
  # optitions should not be included in the template if the variable is not defined which means the template will need to be
  # created dynamically based upon what argparse says is present
  ServiceTemplate = Template('''
define service{
          use                             $inheritance_template
          host_name                       $monitored_instance
          service_description             $service_description
          check_command                   $service_command!$service_command_arg1!$service_command_arg2
          }
  ''')

  # I don't want to use safe substitutions as I want it to error rather than add a bad service check to the configuration file
  ServiceCheck = ServiceTemplate.substitute({ 'inheritance_template': "InheritanceTemplate", 'monitored_instance': "MonitoredInstance", 'service_description': "ServiceDescription", 'service_command': "ServiceCommand", 'service_command_arg1': "CommandArguement1", 'service_command_arg2': "CommandArguement2"})

  # open a file containing a lists of hosts you want to add the check to and read it into a list
  with open(HostConfigList) as f:
     HostList= f.readlines()

  # iterate over the list of hosts
  # still need to find a way to locate the correct file in the filesystem, something along the lines of 'locate -b'
  # currently this will need to be run in the same directory as the configuration files
  i = iter(HostList)
  ConfigFile = i.next() + '.cfg'

  # append the new check to the end of the file
  f = open( "ConfigFile", 'a' )
  f.write(ServiceCheck)
  f.close()

  #print ServiceCheck

if __name__ == "__main__":
    main()
