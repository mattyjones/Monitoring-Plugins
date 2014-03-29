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
  ok_status_exit_code = ceng_lib.ok_status_exit_code
  warning_status_exit_code = ceng_lib.warning_status_exit_code
  critical_status_exit_code = ceng_lib.critical_status_exit_code
  unknown_status_exit_code = ceng_lib.unknown_status_exit_code

  parser = argparse.ArgumentParser(description=' Script that gets the uptime for the current system and makes sure it is above the critical value.')
  parser.add_argument('threshold', type=int, help='the percentage of memory left before entering a critical state')
  parser.add_argument('--no-alert-on-warning', action='store_true', help='disable warning alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument("--no-alert-on-critical", action='store_true', help='disable critical alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--no-alert-on-unknown', action='store_true', help='disable unknown alerts and status\'s for this check (default: yes)')
  args = parser.parse_args()

  # check for a ctitical state, if so and warning is not set to no, then set critical to warning
  critical_status_exit_code = min(1 if args.no_alert_on_critical else 2,
                                0 if args.no_alert_on_warning and args.no_alert_on_critical else 2)
  #print "critical: ", critical_status_exit_code

  # check for a warning state, if so and critical is not set to no, then set warning to critical
  warning_status_exit_code = 0 if args.no_alert_on_warning else 1
  #print "warning: ", warning_status_exit_code

  # if unknown is set to no, then set unknown to ok
  unknown_status_exit_code = 0 if args.no_alert_on_unknown else 3
  #print "unknown: ", unknown_status_exit_code

  if args.threshold:
    Threshold = args.threshold

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
    sys.exit(critical_status_exit_code)
  else:
    if uptime_seconds >= Threshold:
      print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
      sys.exit(warning_status_exit_code)

    elif uptime_seconds <= Threshold:
      print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
      sys.exit(ok_status_exit_code)

if __name__ == "__main__":
    main()
