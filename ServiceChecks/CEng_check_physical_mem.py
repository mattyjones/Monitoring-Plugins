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

import sys
from datetime import datetime
import CEng_python_lib as ceng_lib
import psutil
import argparse

# Get the hostname
machine_name = ceng_lib.get_local_hostname()

def main():

  # enable default alerting
  ok_status_exit_code = ceng_lib.ok_status_exit_code
  warning_status_exit_code = ceng_lib.warning_status_exit_code
  critical_status_exit_code = ceng_lib.critical_status_exit_code
  unknown_status_exit_code = ceng_lib.unknown_status_exit_code

  parser = argparse.ArgumentParser(description='Retrieve the current Memory Utilization of a particular Host.  Additional Performance Data is outputted along with Standard Status Information.')
  parser.add_argument('warning_threshold', type=int, help='the percentage of available memory left before entering a warning state')
  parser.add_argument('critical_threshold', type=int, help='the percentage of memory left before entering a critical state')
  parser.add_argument('--no-alert-on-warning', action='store_true', help='disable warning alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument("--no-alert-on-critical", action='store_true', help='disable critical alerts and dashboard status\'s for this check (default: yes)')
  parser.add_argument('--no-alert-on-unknown', action='store_true', help='disable unknown alerts and status\'s for this check (default: yes)')
  args = parser.parse_args()

  # check for a ctitical state, if so and warning is not set to no, then set critical to warning
  if args.no_alert_on_critical:
    critical_status_exit_code = 1 
    if args.no_alert_on_warning:
        critical_status_exit_code = 0 

  # check for a warning state, if so and critical is not set to no, then set warning to critical
  if args.no_alert_on_warning:
    warning_status_exit_code = 0 

  # if unknown is set to no, then set unknown to ok
  if args.no_alert_on_unknown:
    unknown_status_exit_code = 0 
 
  warning_threshold = args.warning_threshold
  critical_threshold = args.critical_threshold

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

  #print mem_percent

  if mem_percent >= critical_threshold:
    print('Memory Usage Critical - %s%% Usage (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(critical_status_exit_code)

  elif mem_percent >= warning_threshold:
    print('Memory Usage Warning - %s%% Usage (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(warning_status_exit_code)

  else:
    print('Memory Usage OK - %s%% Usage (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
    sys.exit(ok_status_exit_code)

if __name__ == "__main__":
    main()
