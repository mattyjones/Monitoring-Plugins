#! /usr/bin/env python

'''

 CEng_check_http

 Matt Jones caffeinatedengineering@gmail.com
 Created 12.10.13
 Last Update 12.13.13

 Notes:  Script that opens a socket to a remote SSH port and receives the current SSH
         server version and protocol.

 Usage:
 
 Command Line 1:  ./CEng_check_http.py 

 Local Example:  ./CEng_check_http.py
 
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

    #print server

def main():

   # Execution start time
   start_time = datetime.now()

   # Open a socket to port 80
   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   try:
       conn.connect((server, 80))
   except IOError:
       print('There is no service listening on port 80. Make sure the webserver is running and listening on port 80')
       sys.exit(2)
   else:
       pass

   # Check for the desired output
   output = ceng_lib.get_icinga_http_output(conn)
   conn.close()

   run_time = datetime.now() - start_time

   if output:
       print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, run_time))
       sys.exit(0)
   else:
       print('There is a problem with the https server; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
       sys.exit(2)


if __name__ == "__main__":
    main()   


   

       
