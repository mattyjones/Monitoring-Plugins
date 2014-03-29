#! /usr/bin/env python

'''
CEng_check_vol_rw_2

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.12.13
 Last Update 12.12.13

 Notes:  This script checks the "standard" mounts to see if they are read
          only. It also ensures lost+found exists and has the correct
          permissions.
 Usage:

 Command Line 1:  ./CEng_check_rw_2.py --warning <yes/no> --unknown <yes/no> --critical <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_rw_2.py

 Local Example:  /CEng_check_rw_2.py --critical no

'''

from datetime import datetime
import sys
import subprocess
import os
import argparse
import CEng_python_lib as ceng_lib

def main():

  # enable default alerting
  ok_status_exit_code = ceng_lib.ok_status_exit_code
  warning_status_exit_code = ceng_lib.warning_status_exit_code
  critical_status_exit_code = ceng_lib.critical_status_exit_code
  unknown_status_exit_code = ceng_lib.unknown_status_exit_code

  parser = argparse.ArgumentParser(description='This script will get a list of mount points from /proc/self/mounts to see if they are read only.')
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

  # Execution start time
  start_time = datetime.now()

  # Get the uid of the user executing the script
  uid = subprocess.Popen(['id', '-u'], stdout=subprocess.PIPE)
  uid = uid.stdout.read()
  uid = uid.rstrip()

  # This script needs to run as root
  if uid != '0':
    print 'You must be root to run this'
    sys.exit(critical_status_exit_code)
  else:
    pass

  exit_code = ok_status_exit_code

  # The directory to write into
  test_dir = '/lost+found'

  # The mount points to check
  mount_points = ['', '/boot', '/home', '/usr', '/var', '/tmp', '/var/log']

  # List to hold any read-only directories
  ro_dir = []

  i = iter(mount_points)
  for d in mount_points:
    working_directory = i.next() + test_dir
    if not os.path.isdir(working_directory):
      subprocess.Popen(['mkdir', '-m', '0700', working_directory])
    else:
      subprocess.Popen(['chown', '0:0', working_directory])
      subprocess.Popen(['mkdir', 'working_directory', '/.ro'])
      output = subprocess.Popen(['rmdir', 'working_directory', '/.ro'], stdout=subprocess.PIPE)
      output = output.stdout.read()

  if output:
    ro_dir.append(working_directory)
    exit_code = warning_status_exit_code
  else:
    if exit_code != warning_status_exit_code:
      exit_code = ok_status_exit_code

  # The script run time
  run_time = datetime.now() - start_time

  if exit_code == critical_status_exit_code:
    print (ro_dir, ' are Read-Only | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
    sys.exit(exit_code)

  elif exit_code == ok_status_exit_code:
    print ('All directories are Read/Write | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
