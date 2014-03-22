#! /usr/bin/env python

'''

 CEng_add_server.py

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.20.14
 Last Update 03.20.14

 Notes:  This will create a new monitored servered from a clone of an existing monitored server or template

 Usage:

 Command Line 1:  ./CEng_add_server.py

 Local Example:  ./CEng_add_server.py

'''

import sys

def replace_all(text, dic):
  for i, j in dic.iteritems():
    text = text.replace(i, j)
  return text

def main():

  HostConfigList = sys.arg[1] # a list of hostnames to be added to monitoring

  # This is the replacement values that are passed into the search and replace function
  # The new values need to be set dynamically from variables, and the old values should be set from a regex or a known value
  NewValues = {"0.0.0.0": "128.100.10.1", "Default_Host": "NewHostName"}

  # the template to clone from for now all hostnames must be set to default_host and the ip address must be 0.0.0.0
  # this will be chnaged in the future, just now quite sure how to do it robustly yet.
  HostTemplate = sys.argv[2]

  with open(HostConfigList) as f:
    HostList= f.readlines()

  for h in HostList:
    h = h + '.cfg'
    shutil.copy2( HostTemplate,h)
    replace_all(h, NewValues)




if __name__ == "__main__":
    main()
