#! /usr/bin/env python

'''

 CEng_check_ssh

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.17.13

 Notes:  Script that opens a socket to a remote SSH port and receives the current SSH
         server version and protocol.

 Usage:
 
 Command Line 1:  ./CEng_check_ssh.py <hostname> 

 Local Example:  ./CEng_check_ssh.py <hostname>
 
 TODO:

'''  

from datetime import datetime
import socket
import sys

import CEng_python_lib as ceng_lib
import settings as st

# Check to see if a commandline arguement was entered and if so
# attempt to validate it with a regex
if len(sys.argv)  != 2:
    print('Please enter a server to connect to')
    sys.exit(2)
else:
    server = ceng_lib.validate_hostname(sys.argv[1])
    if server:
        server = sys.argv[1]
    else:
        print('Please enter a valid server to connect to')
        sys.exit(2)

def main():

   # Execution start time
   start_time = datetime.now()

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
       result = s.connect_ex((server, 22))
   except IOError:
       print('There is no service listening on port 22. Make sure sshd is running and listening on port 22')
       sys.exit(2)
   else:
       pass

   run_time = datetime.now() - start_time

   if (result == 0):
       output = s.recv(256)
       if not output:
           print('No output was received from SSH, verify that it is running; | \'Check_Time\'=%s;;;0.000000;60.000000;' % ( run_time))
       output = output.rsplit()
       print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output[0], run_time))
       s.close()
       sys.exit(0)

   else:
       print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (st.NO_SOCKET_DATA, run_time))
       s.close()
       sys.exit(2)

if __name__ == "__main__":
    main()   


   

       
