#! /usr/bin/env python

'''

 CEng_check_load

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.30.14
 Last Update 04.01.14

 Notes:  Get the current load average at 1, 5, and 15 minute.  The will function idential to the nagios plugins check_load, which reads from /proc/loadavg.
         The load average is defined as how many processes on average are using the CPU (R status), or waiting for the cpu (D status).  Uptime along with most other utilities read from this file so its trustworthyness is beyond question.
 
 Usage:

 Command Line 1:  ./CEng_check_load.py <Warning_Value> <Critcal_Value> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_load.py -a 20 10

 Local Example:  ./CEng_check_load.py 20 10  --critical no --warning yes

 TODO:

'''

from datetime import datetime
import sys
import argparse
import CEng_python_lib as ceng_lib

def main():

    # enable default alerting
    ok_status_exit_code = ceng_lib.ok_status_exit_code
    warning_status_exit_code = ceng_lib.warning_status_exit_code
    critical_status_exit_code = ceng_lib.critical_status_exit_code
    unknown_status_exit_code = ceng_lib.unknown_status_exit_code

    parser = argparse.ArgumentParser(description='Get the current load average at 1, 5, and 15 minutes')
    parser.add_argument('warning_threshold', type=int, nargs=3, help='the load at which at which a warning state will trigger')
    parser.add_argument('critical_threshold', type=int, nargs=3, help='the load at which a critical state will trigger')
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

    warning_threshold = args.warning_threshold

    critical_threshold = args.critical_threshold

    # Execution start time
    start_time = datetime.now()

    f = open('/proc/loadavg', 'r')
    load = f.readlines()
    f.close()

    one_min_avg = load[0].split()[0]
    five_min_avg = load[0].split()[1]
    fifteen_min_avg = load[0].split()[2]

    # The script run time
    run_time = datetime.now() - start_time
    
    if critical_threshold >= one_min_avg or critical_threshold[1] >= five_min_avg or critical_threshold[2] >= fifteen_min_avg:
        print('The CPU Load Avg has exceeded the critical threshold | \'LoadAvg1\'=%s;%s;%s;0; \'LoadAvg5\'=%s;%s;%s;0; \'LoadAvg15\'=%s;%s;%s;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (one_min_avg, warning_threshold[0], critical_threshold[0], five_min_avg, warning_threshold[1], critical_threshold[1], fifteen_min_avg, warning_threshold[2], critical_threshold[2], run_time))
        sys.exit(critical_status_exit_code)
    elif warning_threshold[0] >= one_min_avg or warning_threshold[1] >= five_min_avg or warning_threshold[2] >= fifteen_min_avg:
        print('The CPU Load Avg has exceeded the warning threshold | \'LoadAvg1\'=%s;%s;%s;0; \'LoadAvg5\'=%s;%s;%s;0; \'LoadAvg15\'=%s;%s;%s;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (one_min_avg, warning_threshold[0], critical_threshold[0], five_min_avg, warning_threshold[1], critical_threshold[1], fifteen_min_avg, warning_threshold[2], critical_threshold[2], run_time))
        sys.exit(critical_status_exit_code)
    elif warning_threshold[0] >= one_min_avg or warning_threshold[1] >= five_min_avg or warning_threshold[2] >= fifteen_min_avg:
        print('The CPU Load Avg has exceeded the warning threshold | \'LoadAvg1\'=%s;%s;%s;0; \'LoadAvg5\'=%s;%s;%s;0; \'LoadAvg15\'=%s;%s;%s;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (one_min_avg, warning_threshold[0], critical_threshold[0], five_min_avg, warning_threshold[1], critical_threshold[1], fifteen_min_avg, warning_threshold[2], critical_threshold[2], run_time))
        sys.exit(warning_status_exit_code)
    else:
        print('The CPU Load Avg is within all thresholds | \'LoadAvg1\'=%s;%s;%s;0; \'LoadAvg5\'=%s;%s;%s;0; \'LoadAvg15\'=%s;%s;%s;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (one_min_avg, warning_threshold[0], critical_threshold[0], five_min_avg, warning_threshold[1], critical_threshold[1], fifteen_min_avg, warning_threshold[2], critical_threshold[2], run_time))
        sys.exit(ok_status_exit_code)


if __name__ == "__main__":
    main()
