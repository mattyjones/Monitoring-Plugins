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

def main():

  # enable default alerting
  OK = ceng_lib.OK
  WARNING = ceng_lib.WARNING
  CRITICAL = ceng_lib.CRITICAL
  UNKNOWN = ceng_lib.UNKNOWN

  parser = argparse.ArgumentParser(description='This script will get a list of mount points from /proc/self/mounts to see if they are read only.')
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

  # Execution start time
  start_time = datetime.now()

  # Get the uid of the user executing the script
  uid = subprocess.Popen(['id', '-u'], stdout=subprocess.PIPE)
  uid = uid.stdout.read()
  uid = uid.rstrip()

  # This script needs to run as root
  if uid != '0':
    print 'You must be root to run this'
    sys.exit(CRITICAL)
  else:
    pass

    ExitCode = OK

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
    exit_code = WARNING
  else:
    if exit_code != WARNING:
      exit_code = OK

  # The script run time
  run_time = datetime.now() - start_time

  if ExitCode == CRITICAL:
    print (ro_dir, ' are Read-Only | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
    sys.exit(ExitCode)

  elif ExitCode == OK:
    print ('All directories are Read/Write | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
    sys.exit(ExitCode)


if __name__ == "__main__":
    main()
