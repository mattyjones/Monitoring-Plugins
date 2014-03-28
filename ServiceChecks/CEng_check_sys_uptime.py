#! /usr/bin/env python
'''
 CEng_check_sys_uptime

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.10.13

 Notes:  Script that gets the uptime for the current system and makes sure it is above the critical value.
           This should be set to five minutes, if it falls below this value then we are aware the
           server has been rebooted rescently.

 Usage:

 Command Line 1:  ./CEng_check_sys_uptime.py <Critcal_Value> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_sys_uptime.py -a 600

 Local Example:  ./CEng_check_sys_uptime.py 600 --critical no

 TODO:
'''


from datetime import datetime
from datetime import timedelta
import sys
import argparse
import CEng_python_lib as ceng_lib

# Get the hostname
machine_name = ceng_lib.get_local_hostname()

def main():

  # The script to run
  base_script = '/proc/uptime'

  # enable default alerting
  OK = ceng_lib.OK
  WARNING = ceng_lib.WARNING
  CRITICAL = ceng_lib.CRITICAL
  UNKNOWN = ceng_lib.UNKNOWN

  parser = argparse.ArgumentParser(description=' Script that gets the uptime for the current system and makes sure it is above the critical value.')
  parser.add_argument('threshold', type=int, help='the percentage of memory left before entering a critical state')
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

  if args['threshold']:
    Threshold = args['threshold']


  # Execution start time
  start_time = datetime.now()

  #with open('/proc/uptime', 'r') as f:
  f = open('/proc/uptime', 'r')
  uptime_seconds = float(f.readline().split()[0])
  output = str(timedelta(seconds = uptime_seconds))

  #The script run time
  run_time = datetime.now() - start_time

  try:
    output
  except NameError: # the above command failed and the script didn't create output
    print('There was a problem accessing the %s, login to %s and verify %s is vaild' &
         (base_script, machine_name, base_script))
    sys.exit(CRITICAL)
  else:
    if uptime_seconds >= Threshold:
      print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
      sys.exit(WARNING)

    elif uptime_seconds <= Threshold:
      print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
      sys.exit(OK)

if __name__ == "__main__":
    main()
