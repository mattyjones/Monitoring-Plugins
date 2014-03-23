#! /usr/bin/env python

'''
CEng_check_cluster

 Matt Jones caffeinatedengineering@gmail.com
 Created 03.10.13
 Last Update 03.13.13

 Notes:  The will use the Icinga Rest API to get all services in a non-ok state and allow you to send out
         a single notification instead of one per host.

 Command Line 1:  ./CEng_check_cluster.py <service description> <critical threshold>

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_cluster.py "NTP Offset" 10

 Local Example:  /CEng_check_cluster.py NTP 10

'''


import json
import requests
import sys

Service = sys.argv[1]
CritThreshold = sys.argv[2]

def main ():

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


  if CritNum > CritThreshold:
      print WarnNum, 'machines warning', CritNum, 'machines critical', UnKnownNum, 'machines Unknown'
      sys.exit(2)
  else:
      print Service, 'is above critical threshold'
      sys.exit(0)

if __name__ == '__main__':
  main()
