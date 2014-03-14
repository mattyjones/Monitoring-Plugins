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

 Command Line 1:  ./CEng_check_rw_2.py

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_rw_2.py

 Local Example:  /CEng_check_rw_2.py

'''

from datetime import datetime
import sys
import subprocess
import os


def main():
    # Execution start time
    start_time = datetime.now()

    # Get the uid of the user executing the script
    uid = subprocess.Popen(['id', '-u'], stdout=subprocess.PIPE)
    uid = uid.stdout.read()
    uid = uid.rstrip()

    # This script needs to run as root
    if uid != '0':
        print 'You must be root to run this'
        sys.exit(3)
    else:
        pass

    exit_code = 0

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
                exit_code = 2
            else:
                if exit_code != 2:
                    exit_code = 0

    # The script run time
    run_time = datetime.now() - start_time

    if exit_code == 2:
        print (ro_dir, ' are Read-Only | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
        sys.exit(exit_code)

    elif exit_code == 0:
        print ('All directories are Read/Write | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
