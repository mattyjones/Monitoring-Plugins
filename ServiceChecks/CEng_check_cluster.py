#! /usr/bin/env python

'''
CEng_check_cluster

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.10.13
 Last Update 03.13.13

 Notes:  The will use the Icinga Rest API to get all services in a non-ok state and allow you to send out
         a single notification instead of one per host.

 Command Line 1:  ./CEng_check_cluster.py --service <service description> --threshold <critical threshold> --warning <yes/no> --critical <yes/no> --unknown <yes/no>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_cluster.py "NTP Offset" 10

 Local Example:  /CEng_check_cluster.py --service "NTP Offset" --threshold 10 --unknown no -- critical yes -- warning no

'''


import json
import requests
import sys
import argparse

def main ():

  # enable default alerting
  OK = 0
  WARNING = 1
  CRITICAL = 2
  UNKNOWN = 3

  parser = argparse.ArgumentParser(description='check_cluster')
  parser.add_argument('--service', help='the service you want to monitor', required=True)
  parser.add_argument('--threshold', help='the threshold at which you wish to trip', required=True)
  parser.add_argument('--warning', help='enable warning alerts and dashboard status\'s for this check, default is yes', required=False)
  parser.add_argument('--critical', help='enable critical alerts and dashboard status\'s for this check, default is yes', required=False)
  parser.add_argument('--unknown', help='enable unknown alerts and status\'s for this check, default is yes', required=False)
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

  if args['service']:
    Service = args['service']

  if args['threshold']:
    Threshold = args['threshold']

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
      sys.exit(CRITICAL)
  else:
      print Service, 'is above  alerting threshold'
      sys.exit(OK)

if __name__ == '__main__':
  main()
