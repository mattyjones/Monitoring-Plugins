#! /usr/bin/env python

'''

 CEng_add_server.py

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.20.14
 Last Update 03.20.14

 Notes:  This will create a new monitored server from a clone of an existing monitored server or template

 Usage:

 Command Line 1:  ./CEng_add_server.py <NewHostList> <HostTemplate>

 Local Example:  ./CEng_add_server.py list_of_hosts.txt server_template.cfg

'''

import sys

def replace_all(NewHost, HostTemplate, NewValues):
 '''
    replace_all
    takes: NewHost HostTemplate, NewValues
    returns: nothing
    function: search fo a dic key and replace it with thecorrsponding dic value
  '''
  
  infile = open(HostTemplate)
  outfile = open(NewHost, 'w')
  for line in infile:
    for i, j in NewValues.iteritems():
      line  = line.replace(i, j)
    outfile.write(line)
  infile.close()
  outfile.close()

def main():

  NewHostList = sys.argv[1] # a list of hostnames to be added to monitoring

  # This is the replacement values that are passed into the search and replace function
  # The new values need to be set dynamically from variables, and the old values should be set from a regex or a known value
  NewValues = {"0.0.0.0": "128.100.10.1", "default_host": "NewHostName"}

  # the template to clone from for now all hostnames must be set to default_host and the ip address must be 0.0.0.0
  # this will be chnaged in the future, just now quite sure how to do it robustly yet.
  HostTemplate = sys.argv[2]

  with open(NewHostList) as f:
    HostList= f.readlines()

  for h in HostList:
    NewHost = h.rstrip()
    NewHost = NewHost + '.cfg'
    replace_all(NewHost, HostTemplate, NewValues)

if __name__ == "__main__":
    main()
