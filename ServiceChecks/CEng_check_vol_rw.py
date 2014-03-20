#! /usr/bin/env python

'''
CEng_check_vol_rw

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.12.13
 Last Update 03.10.14

 Notes:  This script will get a list of mount points from /proc/self/mounts to see if they are read
          only.

 Usage:

 Command Line 1:  ./CEng_check_vol_rw.py

 NRPE Examples   ./check_nrpe -H hal2k1.foo.example.com -c CEng_check_vol_rw.py

 Local Example:  /CEng_check_vol_rw.py

 TODO:

'''

from datetime import datetime
import sys
import subprocess


def main():
    StartTime = datetime.now()
    ExitCode = 0
    # I am using self/mounts so that this will work if the user has namespaces in place, if so then adjust as necessary.
    # Do not use self/mountinfo, while more comprehensive and the 'best' place to go, it is not available prior to 2.26 which rules out < Cent6
    # Do not use mount or mtab as they are staticly generated from fstab and are not updated by select() in realtime
    # For further details please check the inital commit logs for mountinfo or the proc and select manpages
    result = subprocess.Popen(["grep VolGroup /proc/self/mounts | awk '{print $2, $4}' | awk -F, '{print $1}' | awk '{print $2, $1}'"], shell=True, stdout=subprocess.PIPE)
    output = result.stdout.read()
    output = output.strip()
    x = []
    MountPoints = []
    x = output.split('\n')

    # Check to make sure the curent status as reported to the OS is rw
    RWFailDir =  []
    for item in x:
      if 'rw' not in item:
        RWFailDir = item[3:]

    # Create a list of mounts points to write to
    for item in x:
        MountPoints.append(item[3:])

    file = '/.icinga_ro_check' # The file to write, leave the slash it will account for root not being in the list of mount points
    WriteFailDir = []

    i = iter(MountPoints)

    # Attempt to open the file for writing
    for d in MountPoints:
        filepath = i.next() + file
        try:
          f = open( filepath, 'w' )
          f.write(str(StartTime))
          f.close()
        except IOError:
          WriteFailDir.append(filepath)
          ExitCode = 2

    RunTime = datetime.now() - StartTime

    if ExitCode != 0:
      print ('Directories are Read-Only | \'Check_Time\'=%s;;;0.000000;60.000000;' % (RunTime))
      for dir in RWFailDir:
          print dir, 'is not listed as rw according to the OS'
      for dir in WriteFailDir:
        print dir, 'could not be written to'
      sys.exit(ExitCode)

    else:
      print ('All directories are Read/Write | \'Check_Time\'=%s;;;0.000000;60.000000;' % (RunTime))
      sys.exit(ExitCode)


if __name__ == "__main__":
    main()
