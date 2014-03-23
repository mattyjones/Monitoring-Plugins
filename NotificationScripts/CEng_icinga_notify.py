#!/usr/bin/env python

'''

    icinga_notify.py
    Matt Jones caffeinatedengineering@gmail.com
    Created 02.26.14
    Last Update 02.26.14

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


def create_msg():
  MailSender = 'Icinga Monitoring <icinga@' + HostName +'.hal2k1.foo.example.com>'
  IcingaServer = HostName
  msg = MIMEMultipart()
  msg['From'] = MailSender
  msg['To'] = _To
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  try:
    _HostState
  except NameError:
   msg['Subject'] = 'Icinga: ' + _NotificationType + ' service ' + _ServiceName + ' on ' + _HostName + ' is ' _ServiceState
   templateVars = { "NotificationType" : _NotificationType,
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
                   "HostAckComment" : _ServiceAckComment,
                   "HostAckAuthor" : _ServiceAckAuthor,
                   "Escalated" : _Escalated }
   template_file = "/templates/service_email.jinja"
  else:
   msg['Subject'] = 'Icinga: ' + _NotificationType + ' Host ' + _HostName + ' is ' _ServiceState
   templateVars = { "NotificationType" : _NotificationType,
                   "HostName" : _HostName,
                   "HostState" : _HostState,
                   "HostOutput" : _HostOutput,
                   "HostData" : _HostData,
                   "HostGroup" : _HostGroup,
                   "HostAckComment" : _HostAckComment,
                   "HostAckAuthor" : _HostAckAuthor,
                   "IPAddress" : _IPAddress,
                   "EventTime" : _EventTime,
                   "IcingaServer" : IcingaServer,
                   "Escalated" : _Escalated }

   template_file = "/templates/host_email.jinja"
  template = templateEnv.get_template( template_file )
  outputText = template.render( templateVars )
  body = MIMEText(outputText, 'HTML')
  msg.attach(body)
  send_msg(msg, MailSender, _To)

def send_msg(msg, MailSender, _To):
    s = smtplib.SMTP('localhost')
    s.sendmail(MailSender, _To, msg.as_string())
    s.quit()

def main():

  global _NotificationType
  global _ServiceName
  global _ServiceGroup
  global _ServiceState
  global _ServiceOutput
  global _ServiceData
  global _ServiceAckAuthor
  global _ServiceAckComment
  global _HostName
  global _HostState
  global _HostOutput
  global _HostData
  global _HostAckAuthor
  global _HostAckComment
  global _HostGroup
  global _IPAddress
  global _EventTime
  global _Escalated
  global _To

  l = open ("/usr/local/icingadata/tmp/email_log", "a")

  parser = argparse.ArgumentParser(description='Icinga notification email')
  parser.add_argument('--notification_type', help='The type (critical, warning, good, unknown)', required=False)
  parser.add_argument('--service_name', help='The name of the service alerting', required=False)
  parser.add_argument('--service_group', help='The service groups', required=False)
  parser.add_argument('--service_state', help='The state (critical, warning, good, unknown) ', required=False)
  parser.add_argument('--service_output', help='The short service output', required=False)
  parser.add_argument('--service_data', help='The long service output', required=False)
  parser.add_argument('--host_name', help='The name of the host alerting', required=False)
  parser.add_argument('--host_state', help='The host state', required=False)
  parser.add_argument('--host_output', help='The short host output', required=False)
  parser.add_argument('--host_data', help='The long host output', required=False)
  parser.add_argument('--host_group', help='The host groups', required=False)
  parser.add_argument('--ip_address', help='The IP address of the host alerting', required=False)
  parser.add_argument('--event_time', help='The time of the service check', required=False)
  parser.add_argument('--escalated', help='Is this an escalated notification', required=False)
  parser.add_argument('--host_ack_comment', help='The comment associated with the host ack', required=False)
  parser.add_argument('--host_ack_author', help='The author of the host ack', required=False)
  parser.add_argument('--service_ack_comment', help='The comment associated with the service ack', required=False)
  parser.add_argument('--service_ack_author', help='The author of the service ack', required=False)
  parser.add_argument('--to', help='This is who will receive the notification', required=False)
  args = vars(parser.parse_args())

  if args['notification_type']:
    _NotificationType = args['notification_type']
    v = ("Notification Type: " + _NotificationType + "\n")
    l.write(v)

  if args['service_name']:
    _ServiceName = args['service_name']
    v = ("Service Name: " + _ServiceName + "\n")
    l.write(v)

  if args['service_group']:
    _ServiceGroup = args['service_group']
    v =  ("Service group: " + _ServiceGroup + "\n")
    l.write(v)

  if args['service_state']:
    _ServiceState = args['service_state']
    v =  ("Service State" + _ServiceState + "\n")
    l.write(v)

  if args['service_ack_comment']:
    _ServiceAckComment = args['service_ack_comment']
    v =  ("Service Ack Comment: " + _ServiceAckComment + "\n")
    l.write(v)
  else:
      _ServiceAckComment = ''
      v =  ("Service Ack Comment: " + _ServiceAckComment + "\n")
      l.write(v)

  if args['service_ack_author']:
    _ServiceAckAuthor = args['service_ack_author']
    v =  ("Service Ack Author: " + _ServiceAckAuthor + "\n")
    l.write(v)
  else:
        _ServiceAckAuthor = ''
        v =  ("Service Ack Author: " + _ServiceAckAuthor + "\n")
        l.write(v)

  if args['service_output']:
    _ServiceOutput = args['service_output']
    v =  ("Service Short output: " + _ServiceOutput + "\n")
    l.write(v)

  if args['service_data']:
    _ServiceData = args['service_data']
    v =  ("Service Long Output: " + _ServiceData + "\n")
    l.write(v)
  else:
    _ServiceData = ''
    v =  ("Service Long Output: " + _ServiceData + "\n")
    l.write(v)

  if args['host_ack_comment']:
    _HostAckComment = args['host_ack_comment']
    v =  ("Host Ack Comment: " + _HostAckComment + "\n")
    l.write(v)
  else:
      _HostAckComment = ''
      v =  ("Host Ack Comment: " + _HostAckComment + "\n")
      l.write(v)

  if args['host_ack_author']:
    _HostAckAuthor = args['host_ack_author']
    v =  ("Host Ack Author: " + _HostAckAuthor + "\n")
    l.write(v)
  else:
    _HostAckAuthor = ''
    v =  ("Host Ack Author: " + _HostAckAuthor + "\n")
    l.write(v)

  if args['host_name']:
    _HostName = args['host_name']
    v =  ("Host name: " + _HostName + "\n")
    l.write(v)

  if args['to']:
    _To = args['to']
    v =  ("To :" + _To + "\n")
    l.write(v)

  if args['host_state']:
    _HostState = args['host_state']
    v =  ("Host State: " + _HostState + "\n")
    l.write(v)

  if args['host_output']:
    _HostOutput = args['host_output']
    v =  ("Host short output: " + _HostOutput + "\n")
    l.write(v)

  if args['host_data']:
    _HostData = args['host_data']
    v =  ("Host Long Output: " + _HostData + "\n")
    l.write(v)
  else:
    _HostData = ''
    v =  ("Host Long Output: " + _HostData + "\n")
    l.write(v)

  if args['host_group']:
    _HostGroup = args['host_group']
    v =  ("Host group: " + _HostGroup + "\n")
    l.write(v)

  if args['ip_address']:
    _IPAddress = args['ip_address']
    v =  ("IP Address: " + _IPAddress + "\n")
    l.write(v)

  if args['event_time']:
    _EventTime = args['event_time']
    v =  ("Event Time: " + _EventTime + "\n")
    l.write(v)

  if args['escalated']:
    _Escalated = args['escalated']
    v =  ("Escalation Value: " + _Escalated + "\n")
    l.write(v)

  create_msg()



if __name__ == '__main__':
  main()
