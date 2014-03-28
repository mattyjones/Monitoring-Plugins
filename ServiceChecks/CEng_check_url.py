#! /usr/bin/env python

'''

 CEng_check_url

 Matt Jones caffeinatedengineering@gmail.com
 Created 01.24.14
 Last Update 01.24.14

 Notes:  Script that opens a socket to a remote port and receives a stream of data.
         The <url> has to be defined in CEng_python_lib.py in order to be used, follow
         the templates are written there.

 Usage:

 Command Line 1:  ./CEng_check_url.py <hostname> <url> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 Local Example:  ./CEng_check_url.py <hostname> <url> --warning no  --unknown no

 TODO:

'''

from datetime import datetime
import socket
import sys
import re
import argparse
import CEng_python_lib as ceng_lib


def main():

  OK = ceng_lib.OK
  WARNING = ceng_lib.WARNING
  CRITICAL = ceng_lib.CRITICAL
  UNKNOWN = ceng_lib.UNKNOWN

  parser = argparse.ArgumentParser(description='Ppens a socket to a remote port and receives a stream of data.  Follow the examples in CEng_python_lib for examples on verifying output.')
  parser.add_argument('server', help='the hostname of the machine you wish to connect to')
  parser.add_argument('port', type=int, help='the port number you wish to connect to')
  parser.add_argument('url', help='the url you wish to check')
  parser.add_argument('--warning',  choices=['yes', 'no'], default ='yes', help='enable warning alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--critical',  choices=['yes', 'no'], default ='yes', help='enable critical alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--unknown',  choices=['yes', 'no'],  default ='yes', help='enable unknown alerts and status\'s for this check (default: yes)')
  args = vars(parser.parse_args())
  
  # check for a ctitical state, if so and warning is not set to no, then set critical to warning
  if args['critical']:
    if args['critical'] == 'no' and args['warning'] == 'no':
      CRITICAL = OK
    elif args['critical'] == 'no' and args['warning'] != 'no':
      CRITICAL = WARNING
  else:
    CRITICAL = CRITICAL
  
  # check for a warning state, if so and critical is not set to no, then set warning to critical
  if args['warning']:
    if args['warning'] == 'no' and args['critical'] == 'no':
      WARNING = OK
    elif args['warning'] == 'no' and args['critical'] != 'no':
      WARNING = OK
  else:
    WARNING = WARNING 
  
  # if unknown is set to no, then set unknown to ok
  if args['unknown']:
    if args['unknown'] == 'no':
      UNKNOWN = OK
    else:
      UNKNOWN = UNKNOWN

  if args['port']:
    Port = args['port'] 

  if args['server']:
    Server = ceng_lib.validate_hostname(args['server'])
    if Server:
      Server = args['server']
    else:
      print "Please enter a valid hostname to connect to"
      sys.exit('CRITICAL')

  if args['url']:
    Url = args['url'] 

  
  # Execution start time
  start_time = datetime.now()


  # Open a socket to port a port
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    conn.connect((Server, Port))
  except IOError:
    print('There is no service listening on port 8080. Make sure the service is running and listening on port 8080')
    sys.exit(CRITICAL)
   else:
     pass


  # Check for the desired output
  if Url == 'root':
    output = ceng_lib.get_port_output(conn)
    conn.close()
  elif Url == 'icinga-web':
    output = ceng_lib.get_icinga_http_output(conn)
    run_time = datetime.now() - start_time

  if output:
    print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, run_time))
    sys.exit(OK)
  else:
       print('There is a problem with the service on the server; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
       sys.exit(CRITICAL)

if __name__ == "__main__":
    main()
