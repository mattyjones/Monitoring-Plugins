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

 Command Line 1:  ./CEng_check_sys_uptime.py <Critcal_Value>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_sys_uptime.py -a 600

 Local Example:  ./CEng_check_sys_uptime.py 600

 TODO:
'''


from datetime import datetime
from datetime import timedelta
import sys

import CEng_python_lib as ceng_lib

# Get the commandline argumentts
uptime_critical  = sys.argv[1]

# The script to run
base_script = '/proc/uptime'

# Get the hostname
machine_name = ceng_lib.get_local_hostname()

def main():

   try:
       uptime_critical
   except NameError:
       print('Please enter a value for [uptime_critical]')
   else:
       pass

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
      sys.exit(3)
   else:
      if uptime_seconds >= uptime_critical:
         print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
         sys.exit(2)

      elif uptime_seconds <= uptime_critical:
         print('Uptime: %s | \'System Uptime\'=%s;0.00;1.0;0.00;10000000000; \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, output, run_time))
         sys.exit(0)

if __name__ == "__main__":
    main()
