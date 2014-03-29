#! /usr/bin/env python

'''
CEng_check_cluster

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.10.13
 Last Update 03.13.13

 Notes:  The will use the Icinga Rest API to get all services in a non-ok state and allow you to send out
         a single notification instead of one per host.

 Command Line 1:  ./CEng_check_cluster.py <service description> <critical threshold> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_cluster.py "NTP Offset" 10

 Local Example:  /CEng_check_cluster.py "NTP Offset" 10 --unknown no -- critical yes -- warning no

'''


import json
import requests
import sys
import argparse
import CEng_python_lib as ceng_lib

def main ():

  # enable default alerting
  ok_status_exit_code = ceng_lib.ok_status_exit_code
  warning_status_exit_code = ceng_lib.warning_status_exit_code
  critical_status_exit_code = ceng_lib.critical_status_exit_code
  unknown_status_exit_code = ceng_lib.unknown_status_exit_code

  parser = argparse.ArgumentParser(description=' The will use the Icinga Rest API to get all services in a non-ok state and allow you to send out a single notification instead of one per host.')
  parser.add_argument('service', help='the service you want to monitor')
  parser.add_argument('threshold', type=int, help='the threshold at which you wish to trip')
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

  if args.service:
    Service = args.service

  if args.threshold:
    Threshold = args.threshold

  CritNum = 0
  WarnNum = 0
  UnKnownNum = 0

  Url = 'hostname/icinga-web/web/api/service/filter[AND(HOST_CURRENT_STATE|=|0;OR(SERVICE_CURRENT_STATE|!=|0;))]/columns[HOST_NAME|SERVICE_NAME|SERVICE_CURRENT_STATE]/order[SERVICE_CURRENT_STATE;DESC]/authkey=xxx/json'
  r = requests.get(Url)
  JsonData = {}
  JsonData = r.json()

  for item in JsonData['result']:

    if Service in item.values():
      if item.get('SERVICE_CURRENT_STATE') == '1':
        WarnNum = WarnNum + 1
      elif item.get('SERVICE_CURRENT_STATE') == '2':
        CritNum = CritNum + 1
      elif item.get('SERVICE_CURRENT_STATE') == '3':
        UnKnownNum = UnKnownNum + 1

  AlertNum = WarnNum + CritNum + UnKnownNum

  if AlertNum > Threshold:
      print WarnNum, 'machines warning', CritNum, 'machines critical', UnKnownNum, 'machines Unknown'
      sys.exit(critical_status_exit_code)
  else:
      print Service, 'is above  alerting threshold'
      sys.exit(ok_status_exit_code)

if __name__ == '__main__':
  main()
