#!/usr/bin/env python

'''

    CEng_update_icinga.py
    Matt Jones caffeinatedengineering@gmail.com
    Created 02.22.14
    Last Update 02.25.14

    Notes:


    Usage:


    ToDo:


'''

import subprocess
import os
import shutil
import sys
import smtplib
import socket
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import jinja2


GitBranch = 'master'
GitRepo = 'origin'
BaseRepoDirectory = '/path/to/repo'
ConfigFiles = ['commands.cfg', 'contacts.cfg', 'groups.cfg', 'templates.cfg', 'timeperiods.cfg', 'dependency.cfg']
BaseLocalDirectory = '/path/to/local_configuration'
RepoList = [' ', ' ', ' ', ' ']

HostName = socket.gethostname()
HostName = HostName.split('.')
HostName = HostName[0]
ServiceList = ['httpd', 'ido2db', 'icinga', 'nrpe']


def get_host():
  HostName = socket.gethostname()
  HostName = HostName.split('.')
  HostName = HostName[0]
  return HostName

def create_msg(RepoName, RepoOutput, GitModifiedFiles, CheckStatus):
  ServiceInfo = get_service_state_info()
  MailSender = 'Icinga Monitoring <icinga@' + HostName + '.be.monster.com>'
  To = 'hal@hal2k1.foo.example.com'
  msg = MIMEMultipart()
  msg['Subject'] = 'Icinga Configuration Status'
  msg['From'] = MailSender
  msg['To'] = To
  repo_msg = []
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  template_file = "/templates/git_email.jinja"
  template = templateEnv.get_template( template_file )
  templateVars = { "RepoName" : RepoName,
                   "RepoOutput" : RepoOutput,
                   "GitModifiedFiles" : GitModifiedFiles,
                   "ServiceList" : ServiceList,
                   "ServiceInfo" : ServiceInfo,
                   "CheckStatus" : CheckStatus  }
  outputText = template.render( templateVars )

  body = MIMEText(outputText, 'HTML')
  msg.attach(body)
  send_msg(msg, MailSender, To)

def send_msg(msg, MailSender, To):
    s = smtplib.SMTP('localhost')
    s.sendmail(MailSender, To, msg.as_string())
    s.quit()


def get_service_state_info():
  '''
    get_service_state_info
    takes: nothing
    returns: nothing
    this will get the current state and last restart of a service

  '''
  ServiceInfo = {}
  test = []
  for service in ServiceList:
      cmd = 'ps -C ' + service + ' -o lstart | grep -iv started | sort -h | head -n1'
      result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      out, err = result.communicate()

      if out:
          test.append((service, 'UP', out))
      else:
          test.append((service, 'DOWN', out))
  for service, state, restart in test:
          ServiceInfo.setdefault(service, {})[state] = restart

  return ServiceInfo



def pull_repo(repo):
  '''
    pull_repo
    takes: nothing
    returns: nothing
    this funtion will pull a given repo

  '''

  output = subprocess.Popen(['git pull', GitRepo, GitBranch], shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  out, err = output.communicate()
  return out

def update_config_files(repo):
  '''
    update_config_files
    takes: nothing
    returns:nothing
    this will only run if the hash has changed.  It will delete all files in the local config
    directories and then copy in the files from the repo.

  '''

  DestConfigPath = BaseLocalDirectory  + '/icinga_configuration/'
  DestDeployedPath = BaseLocalDirectory + '/deployed_servers/'
  SrcDeployedPath = BaseRepoDirectory + '/' + repo + '/deployed/' + HostName + '/'
  SrcConfigPath = BaseRepoDirectory + '/' + repo + '/'

  for file in os.listdir(DestConfigPath):
    file = os.path.join(DestConfigPath, file)
    os.remove(file)

  for file in os.listdir(DestDeployedPath):
    file = os.path.join(DestDeployedPath, file)
    os.remove(file)

  for file in ConfigFiles:
    SrcConfigFile = os.path.join(SrcConfigPath,file)
    shutil.copy(SrcConfigFile, DestConfigPath)

  for file in os.listdir(SrcDeployedPath):
    SrcDeployedFile = os.path.join(SrcDeployedPath, file)
    shutil.copy(SrcDeployedFile, DestDeployedPath)


def restart_service():
  '''
    restart_service
    takes: nothing
    returns: nothing
    This will restart all icinga releated services

  '''
  subprocess.Popen(["service nrpe restart"], shell = True, stdout=subprocess.PIPE)
  subprocess.Popen(["service ido2db restart"], shell = True, stdout=subprocess.PIPE)
  subprocess.Popen(["service icinga restart"], shell = True, stdout=subprocess.PIPE)

def check_icinga_config():
  '''
    check_icinga_config
    takes: nothing
    returns: output
    This will run a test of the new configuration before going live.  If there are any errors no services
    will be started and the current running config will be left intact.

  '''

  output = subprocess.Popen(['/usr/bin/icinga', '-v', '/etc/icinga/icinga.cfg'], stdout=subprocess.PIPE)
  output = output.stdout.read()
  if 'Total Warnings: 0' in output and 'Total Errors:   0' in output:
      restart_service()
  else:
      return output


def main():

  RepoName = []
  RepoOutput = {}
  CheckStatus = " "
  GitModifiedFiles = []
  for repo in RepoList:
      path = BaseRepoDirectory + '/' + repo
      os.chdir(path)
      git_output = subprocess.Popen(["git log | head -n1 | awk '{print $2}'"], shell=True, stdout=subprocess.PIPE)
      git_before = git_output.stdout.read()
      repo_status = pull_repo(repo)
      git_output = subprocess.Popen(["git log | head -n1 | awk '{print $2}'"], shell=True, stdout=subprocess.PIPE)
      git_after = git_output.stdout.read()
      RepoName.append(repo)
      RepoOutput[RepoName.index(repo)] = repo_status
      if 'error' in RepoOutput[RepoName.index(repo)]:
          pass
      else:
          if "Already up-to-date" not in RepoOutput[RepoName.index(repo)]:
              RepoOutput[RepoName.index(repo)] = "Updated"
          if git_before != git_after:
              cmd = "git diff --name-status " + git_before + " " + git_after
              with open(os.devnull, "w") as devnull:
                  result = subprocess.Popen(cmd, shell=True, stderr=devnull, stdout=subprocess.PIPE)
              out = result.stdout.read()
              out = out.splitlines()
              for item in out:
                  GitModifiedFiles.append(item.split("\t"))
              if repo == 'configuration_files':
                update_config_files(repo)
                config_status = check_icinga_config()
                if config_status:
                    CheckStatus = "Configuration Verifaction Failed"
                else:
                    CheckStatus = "Configuration Verification Passed"

  create_msg(RepoName, RepoOutput, GitModifiedFiles, CheckStatus)
  print "All is well that ends well"

if __name__ == '__main__':
  main()
