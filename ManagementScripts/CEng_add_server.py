#! /usr/local/icingadata/store/icinga_management_scripts/lang/bin/python2.7

'''

 CEng_add_server.py

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.20.14
 Last Update 03.20.14

 Notes:  This will create a new monitored server from a clone of an existing monitored server or template

 Usage:

 Command Line 1:  ./CEng_add_server.py <new_host_list> <host_template>

 Local Example:  ./CEng_add_server.py list_of_hosts.txt server_template.cfg

'''

import sys

def replace_all(new_host, host_template, new_values):
  '''
    replace_all
    takes: new_host host_template, new_values
    returns: nothing
    function: search fo a dic key and replace it with thecorrsponding dic value
  '''

  infile = open(host_template)
  outfile = open(new_host, 'w')
  for line in infile:
    for i, j in new_values.iteritems():
      line  = line.replace(i, j)
    outfile.write(line)
  infile.close()
  outfile.close()

def main():

  new_host_list = sys.argv[1] # a list of hostnames to be added to monitoring

  # This is the replacement values that are passed into the search and replace function
  # The new values need to be set dynamically from variables, and the old values should be set from a regex or a known value
  new_values = {"0.0.0.0": "128.100.10.1", "default_host": "new_hostName"}

  # the template to clone from for now all hostnames must be set to default_host and the ip address must be 0.0.0.0
  # this will be chnaged in the future, just now quite sure how to do it robustly yet.
  host_template = sys.argv[2]

  with open(new_host_list) as f:
    HostList= f.readlines()

  for h in HostList:
    new_host = h.rstrip()
    new_host = new_host + '.cfg'
    replace_all(new_host, host_template, new_values)

if __name__ == "__main__":
    main()
