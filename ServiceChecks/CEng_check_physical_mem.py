#! /usr/bin/env python

'''

 icinga_check_memory

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.10.13

 Notes:  Script that retrieves the current Memory Utilization of a particular Host.
          Additional Performance Data is outputted along with Standard Status Information.


 Usage:

 Command Line 1:  ./icinga_check_memory.py <Warning_Value> <Critcal_Value> --warning <yes/no> --critical <yes/no> --unknown <yes/no> 

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c icinga_check_memory.py -a 20 10

 Local Example:  ./icinga_check_memory.py 20 10  --critical no --warning yes

 TODO:

'''

from datetime import datetime
import sys
import subprocess
import psutil
import argparse
import CEng_python_lib as ceng_lib

# Get the hostname
machine_name = ceng_lib.get_local_hostname()

def main():

 # enable default alerting
  OK = 0
  WARNING = 1
  CRITICAL = 2
  UNKNOWN = 3

  parser = argparse.ArgumentParser(description='Retrieve the current Memory Utilization of a particular Host.  Additional Performance Data is outputted along with Standard Status Information.')
  parser.add_argument('warning_threshold', type=int, help='the percentage of available memory left before entering a warning state')
  parser.add_argument('critical_threshold', type=int, help='the percentage of memory left before entering a critical state')
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

  if args['warning_threshold']:
    WarningThreshold = args['warning_threshold']

  if args['critical_threshold']:
    CriticalThreshold = args['critical_threshold']

  # Execution start time
  start_time = datetime.now()

  # Get the memory stat
  memory = psutil.virtual_memory()

  # The script run time
  run_time = datetime.now() - start_time


  mem_total = memory[0] /1048876
  mem_percent = memory[2]
  mem_free = memory[4] /1048876
  mem_active = memory[5] /1048876
  mem_caches = ( memory[7] + memory[8] ) /1048876

  if memory[2] >= CriticalThreshold:
    print('Memory Usage Critical - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(CRITICAL)

  elif memory[2] >= WarningThreshold:
    print('Memory Usage Warning - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(WARNING)

  else:
    print('Memory Usage OK - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(OK)

if __name__ == "__main__":
    main()
