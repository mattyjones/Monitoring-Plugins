#! /usr/bin/env python

'''

    icinga_notify.py
    Matt Jones caffeinatedengineering@gmail.com
    Created 02.26.14
    Last Update 04.09.14

    Notes:


    Usage:


    ToDo:


'''

import os
import argparse
import sys
import smtplib
import socket
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import jinja2

HostName = socket.gethostname()
HostName = HostName.split('.')
HostName = HostName[0]
IcingaServer = HostName

def create_msg(template_vars, alert, _To):
  MailSender = 'Icinga Monitoring <svcicinga@' + HostName +'.be.monster.com>'
  msg = MIMEMultipart()
  msg['From'] = MailSender
  msg['To'] = _To
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  if alert == "service":
    msg['Subject'] = "IcingaQA: " + _NotificationType + " service " + _ServiceName + " on " + _HostName + " is " + _ServiceState
    template_file = "/usr/local/icingadata/store/icinga_management_scripts/templates/service_email.jinja"
  elif alert == "host":  
    msg['Subject'] = 'IcingaQA: ' + _NotificationType + ' Host ' + _HostName + ' is ' +  _HostState
    template_file = "/usr/local/icingadata/store/icinga_management_scripts/templates/host_email.jinja"
  template = templateEnv.get_template( template_file )
  output_text = template.render( template_vars )
  body = MIMEText(output_text, 'HTML')
  msg.attach(body)
  send_msg(msg, MailSender, _To)

def send_msg(msg, MailSender, _To):
    s = smtplib.SMTP('localhost')
    s.sendmail(MailSender, _To, msg.as_string())
    s.quit()

def main():

  global _NotificationType
  global _ServiceName
  global _ServiceState
  global _HostName
  global _HostState

  parser = argparse.ArgumentParser(description='Icinga notification email')
  parser.add_argument('notification_type', help='The type (critical, warning, good, unknown)')
  parser.add_argument('host_name', help='The name of the host alerting')
  parser.add_argument('--host_state', help='The host state')
  parser.add_argument('host_group', help='The host groups')
  parser.add_argument('ip_address', help='The IP address of the host alerting')
  parser.add_argument('event_time', help='The time of the service check')
  parser.add_argument('escalated', help='Is this an escalated notification')
  parser.add_argument('to', help='This is who will receive the notification')
  parser.add_argument('--host_output', help='the short host output')
  parser.add_argument('--host_data', help='the long host output')
  parser.add_argument('--service_name', help='The name of the service alerting')
  parser.add_argument('--service_group', help='The service groups')
  parser.add_argument('--service_state', help='The state (critical, warning, good, unknown)')
  parser.add_argument('--service_output', help='The short service output')
  parser.add_argument('--service_data', help='The long service output')
  args = vars(parser.parse_args())

  _NotificationType = args['notification_type']
  _ServiceName = args['service_name']
  _ServiceGroup = args['service_group']
  _ServiceState = args['service_state']
  _ServiceOutput = args['service_output']
  if args['service_data']:
    _ServiceData = args['service_data']
  else:
    _ServiceData = 'None'
  _HostName = args['host_name']
  _To = args['to']
  _HostState = args['host_state']
  _HostOutput = args['host_output']
  if args['host_data']:
    _HostData = args['host_data']
  else:
    _HostData = 'None'
  _HostGroup = args['host_group']
  _IPAddress = args['ip_address']
  _EventTime = args['event_time']
  if args['escalated'] == '0':
    _Escalated = 'This message is NON-ACTIONABLE and has not been seen by the GOC'
  elif args['escalated'] == '1':
    _Escalated = 'This is ACTIONABLE and the app owner has been aware for 24 hours'

  if not _ServiceName:
    alert = "host"
    template_vars = { "NotificationType" : _NotificationType,
                     "HostName" : _HostName,
                     "HostState" : _HostState,
                     "HostOutput" : _HostOutput,
                     "HostData" : _HostData,
                     "HostGroup" : _HostGroup,
                     "IPAddress" : _IPAddress,
                     "EventTime" : _EventTime,
                     "IcingaServer" : IcingaServer,
                     "Escalated" : _Escalated }
  else:
    alert = "service"
    template_vars = { "NotificationType" : _NotificationType,
                     "ServiceName" : _ServiceName,
                     "ServiceGroup" : _ServiceGroup,
                     "ServiceState" : _ServiceState,
                     "ServiceOutput" : _ServiceOutput,
                     "ServiceData" : _ServiceData,
                     "HostName" : _HostName,
                     "HostGroup" : _HostGroup,
                     "IPAddress" : _IPAddress,
                     "EventTime" : _EventTime,
                     "IcingaServer" : IcingaServer,
                     "Escalated" : _Escalated }

  create_msg(template_vars, alert, _To)

if __name__ == '__main__':
  main()
