#! /usr/bin/env python

'''

 CEng_check_ssh

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.17.13

 Notes:  Script that opens a socket to a remote SSH port and receives the current SSH
         server version and protocol.

 Usage:

 Command Line 1:  ./CEng_check_ssh.py <hostname> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 Local Example:  ./CEng_check_ssh.py <hostname> --warning no --unknown no

 TODO:

'''

from datetime import datetime
import socket
import sys
import argparse
import CEng_python_lib as ceng_lib

def main():

  # enable default alerting
  ok_status_exit_code = ceng_lib.ok_status_exit_code
  warning_status_exit_code = ceng_lib.warning_status_exit_code
  critical_status_exit_code = ceng_lib.critical_status_exit_code
  unknown_status_exit_code = ceng_lib.unknown_status_exit_code

  parser = argparse.ArgumentParser(description='Open a socket to a remote SSH port and receives the current SSH server version and protocol.')
  parser.add_argument('server', help='the server you wish to connect to')
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

  if args.server:
    server = ceng_lib.validate_hostname(args.server)
    if server:
      server = args.server
  else:
    print "Please enter a valid hostname to connect to"
    sys.exit(critical_status_exit_code)


  # Execution start time
  start_time = datetime.now()

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    result = s.connect_ex((server, 22))
  except IOError:
    print('There is no service listening on port 22. Make sure sshd is running and listening on port 22')
    sys.exit(critical_status_exit_code)
  else:
    pass

  run_time = datetime.now() - start_time

  if (result == 0):
    output = s.recv(256)
    if not output:
      print('No output was received from SSH, verify that it is running; | \'Check_Time\'=%s;;;0.000000;60.000000;' % ( run_time))
      s.close()
      sys.exit(critical_status_exit_code)
    output = output.rsplit()
    print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output[0], run_time))
    s.close()
    sys.exit(ok_status_exit_code)

  else:
    print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % ('No data was received from the socket', run_time))
    s.close()
    sys.exit(critical_status_exit_code)

if __name__ == "__main__":
    main()
