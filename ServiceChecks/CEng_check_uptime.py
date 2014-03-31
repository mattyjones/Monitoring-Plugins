#! /usr/bin/env python

'''

 CEng_check_uptime

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.31.14
 Last Update 03.31.14

 Notes:  Get the current system uptime
 
 Usage:

 Command Line 1:  ./CEng_check_uptime.py <Threshold> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_load.py -a 300 

 Local Example:  ./CEng_check_uptime.py 300  --critical no --warning yes

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

    parser = argparse.ArgumentParser(description='Get the current system uptime')
    parser.add_argument('threshold', type=int, help='the uptime at which at which an alert will trigger if below')
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

    #if args.critical_threshold:
    alert_threshold = args.threshold

    # Execution start time
    start_time = datetime.now()

    f = open('/proc/uptime', 'r')
    sys_uptime = f.readlines()
    f.close()

    sys_uptime_seconds = sys_uptime[0].split()[0]
    sys_uptime_days = int(float(sys_uptime_seconds) / 86400)

    # The script run time
    run_time = datetime.now() - start_time
    
    if sys_uptime_seconds <= alert_threshold:
        print('The system uptime is less than %s | \'sys_uptime\'=%s;0;0;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (sys_uptime_seconds, sys_uptime_days, run_time))
        sys.exit(critical_status_exit_code)
    else:
        print('The system has been up for %s days | \'sys_uptime\'=%s;0;0;0; \'Check_Time\'=%s;;;0.000000;60.000000;' % 
             (int(sys_uptime_days), sys_uptime_days, run_time))
        sys.exit(ok_status_exit_code)

if __name__ == "__main__":
    main()
