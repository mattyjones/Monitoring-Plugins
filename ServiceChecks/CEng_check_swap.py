#! /usr/bin/env python

'''

 CEng_check_swap

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 1.10.14

 Notes:  Script that retrieves the current Memory Utilization of a particular Host.
          Additional Performance Data is outputted along with Standard Status Information.


 Usage:

 Command Line 1:  ./CEng_check_swap.py <Warning_Value> <Critcal_Value>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c check_swap.py -a 20 10

 Local Example:  ./CEng_check_swap.py 20 10

 TODO:

'''

from datetime import datetime
import sys
#import subprocess
import psutil

import CEng_python_lib as ceng_lib
#import settings

if len(sys.argv) != 3:
    print('Please enter a warning and critical value')
    sys.exit(2)

# Get the hostname
machine_name = ceng_lib.get_local_hostname()


def main():
    swap_warning = sys.argv[1]
    swap_critical = sys.argv[2]

    try:
        swap_warning, swap_critical
    except NameError:
        print('Please enter a value for [swap_warning] and [swap_critical]')
    else:
        pass

    # Execution start time
    start_time = datetime.now()

    # Get the memory stat
    memory = psutil.swap_memory()

    # The script run time
    run_time = datetime.now() - start_time

    swap_total = memory[0] / 1048876
    swap_percent = memory[3]
    swap_used = memory[1] / 1048876

    if memory[2] >= swap_critical:
        print(
        'Memory Usage Warning - %s (%sMB out of %sMB); | Swap=%sMB;0;0;0;%sMB; \'Check_Time\'=%s;;;0.000000;60.000000;' % (
        swap_percent,
        swap_used,
        swap_total,
        swap_total,
        swap_total,
        run_time))
        sys.exit(2)

    elif memory[2] >= swap_warning:
        print(
        'Memory Usage Warning - %s (%sMB out of %sMB); | Swap=%sMB;0;0;0;%sMB; \'Check_Time\'=%s;;;0.000000;60.000000;' % (
        swap_percent,
        swap_used,
        swap_total,
        swap_total,
        swap_total,
        run_time))
        sys.exit(1)

    else:
        print(
        'Memory Usage Warning - %s (%sMB out of %sMB); | Swap=%sMB;0;0;0;%sMB; \'Check_Time\'=%s;;;0.000000;60.000000;' % (
        swap_percent,
        swap_used,
        swap_total,
        swap_total,
        swap_total,
        run_time))
        sys.exit(0)


if __name__ == "__main__":
    main()








