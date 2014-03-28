#! /usr/bin/env python

'''

 CEng_check_http

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.13.13

 Notes:  Script that opens a socket to a remote SSH port and receives the current SSH
         server version and protocol.

 Usage:

 Command Line 1:  ./CEng_check_http.py <server> --warning <yes/no> --unknown <yes/no> --critical <yes/no>

 Local Example:  ./CEng_check_http.py hal2k1.foo.example.com --critical yes

 TODO:

'''

from datetime import datetime
import socket
import sys
import argparse
import CEng_python_lib as ceng_lib

def main():
 
  # enable default alerting
  OK = 0
  WARNING = 1
  CRITICAL = 2
  UNKNOWN = 3

  parser = argparse.ArgumentParser(description='Open a socket to a remote SSH port and receives the current SSH
         server version and protocol.')
  parser.add_argument('server', help='the server you wish to connect to')
  parser.add_argument('--warning', choices=['yes', 'no'], default ='yes', help='enable warning alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--critical', choices=['yes', 'no'], default ='yes', help='enable critical alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--unknown', choices=['yes', 'no'], default ='yes', help='enable unknown alerts and status\'s for this check (default: yes)')
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

  if args['server']:
    server = ceng_lib.validate_hostname(args['server'])
    if server:
      server = args['server']
  else:
    print "Please enter a valid hostname to connect to"
    sys.exit('CRITICAL')


  # Execution start time
  start_time = datetime.now()

  # Open a socket to port 80
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    conn.connect((server, 80))
  except IOError:
    print('There is no service listening on port 80. Make sure the webserver is running and listening on port 80')
    sys.exit(CRITICAL)
  else:
   pass

  # Check for the desired output
  output = ceng_lib.get_icinga_http_output(conn)
  conn.close()

  run_time = datetime.now() - start_time
  if output:
    print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, run_time))
    sys.exit(OK)
  else:
    print('There is a problem with the https server; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
    sys.exit(CRITICAL)

if __name__ == "__main__":
    main()
