#! /usr/bin/env python

'''

 icinga_check_memory

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.10.13

 Notes:  Script that retrieves the current Memory Utilization of a particular Host.
          Additional Performance Data is outputted along with Standard Status Information.


 Usage:

 Command Line 1:  ./icinga_check_memory.py <Warning_Value> <Critcal_Value>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c icinga_check_memory.py -a 20 10

 Local Example:  ./icinga_check_memory.py 20 10

 TODO:

'''

from datetime import datetime
import sys
import subprocess
import psutil

import CEng_python_lib as ceng_lib
import settings

# Get the commandline argumentts
mem_warning = sys.argv[1]
mem_critical  = sys.argv[2]

# Get the hostname
machine_name = ceng_lib.get_local_hostname()

def main():

   try:
       mem_warning, mem_critical
   except NameError:
       print('Please enter a value for [mem_warning] and [mem_critical]')
   else:
       pass

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

   if memory[2] >= mem_critical:
       print('Memory Usage Critical - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
       sys.exit(2)

   elif memory[2] >= mem_warning:
       print('Memory Usage Warning - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
       sys.exit(1)

   else:
       print('Memory Usage OK - %s (%sMB)Active; | Total=%sMB;;;; Active=%sMB;;;; Free=%sMB;;;; Cached=%sMB;;;; \'Check_Time\'=%s;;;0.000000;60.000000;' % (mem_percent,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_total,
                                                                                                                                                                         mem_active,
                                                                                                                                                                         mem_free,
                                                                                                                                                                         mem_caches,
                                                                                                                                                                         run_time))
       sys.exit(0)

if __name__ == "__main__":
    main()
