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
import argparse

def main():

  parser = argparse.ArgumentParser(description='Add new service check')
  parser.add_argument('--InheritanceTemplate', help='a seperate service definition template you wish to inherit from', required=False)
  parser.add_argument('--MonitoredInstance', help='the hostname of the server you wish to monitor', required=True)
  parser.add_argument('--ServiceDescription', help='this will define the description of the service', required=True)
  parser.add_argument('--ServiceCommand', help='the command used to run the service, must be defined in a command file first', required=True)
  parser.add_argument('--CommandArguement1', help='the first commandline arguement', required=False)
  parser.add_argument('--CommandArguement2', help='the second commandline arguement', required=False)
  parser.add_argument('--CommandArguement3', help='the third commandline arguement', required=False)
  parser.add_argument('--HostConfigList', help='a list of hosts you wish to add the check to', required=True)
  args = vars(parser.parse_args())

  if args['InheritanceTemplate']:
    InheritanceTemplate = args['InheritanceTemplate']
  else:
    InheritanceTemplate = ''
  
  if args['MonitoredInstance']:
    MonitoredInstance = args['MonitoredInstance']
  
  if args['ServiceDescription']:
    ServiceDescription = args['ServiceDescription']
  
  if args['ServiceCommand']:
    ServiceCommand = args['ServiceCommand']
    ServiceCommandLine = "$service_command"
  
  if args['CommandArguement1']:
    CommandArguement1 = args['CommandArguement1']
    ServiceCommand = ServiceCommand + "!" + CommandArguement1
  
  if args['CommandArguement2']:
    CommandArguement2 = args['CommandArguement2']
    ServiceCommand = ServiceCommand + "!" + CommandArguement2
  
  if args['CommandArguement3']:
    CommandArguement3 = args['CommandArguement3']
    ServiceCommand = ServiceCommand + "!" + CommandArguement3
  
  if args['HostConfigList']:
    HostConfigList = args['HostConfigList']
  

  # a very basic service definition, a better one with all available optitions needs to be created
  # optitions should not be included in the template if the variable is not defined which means the template will need to be
  # created dynamically based upon what argparse says is present
  
  if InheritanceTemplate:
    ServiceTemplate = Template('''
define service{
          use                             $inheritance_template
          host_name                       $monitored_instance
          service_description             $service_description
          check_command                   $service_command
          }
  ''')
  else:
    ServiceTemplate = Template('''
define service{
          host_name                       $monitored_instance
          service_description             $service_description
          check_command                   $service_command
          }
  ''')


  # I don't want to use safe substitutions as I want it to error rather than add a bad service check to the configuration file
  ServiceCheck = ServiceTemplate.substitute({ 'inheritance_template': InheritanceTemplate, 'monitored_instance': MonitoredInstance, 'service_description': ServiceDescription, 'service_command': ServiceCommand})
  
  # open a file containing a lists of hosts you want to add the check to and read it into a list
  with open(HostConfigList) as hl:
     HostList= hl.readlines()
  
  # iterate over the list of hosts
  # still need to find a way to locate the correct file in the filesystem, something along the lines of 'locate -b'
  # currently this will need to be run in the same directory as the configuration files
  i = iter(HostList)
  ConfigFile = i.next().rstrip() + '.cfg'
  
  # append the new check to the end of the file
  f = open( ConfigFile, 'a' )
  f.write(ServiceCheck)
  f.close()
  hl.close()

if __name__ == "__main__":
    main()
