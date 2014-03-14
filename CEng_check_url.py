#! /usr/bin/env python

'''

 CEng_check_url

 Matt Jones caffeinatedengineering@gmail.com
 Created 01.24.14
 Last Update 01.24.14

 Notes:  Script that opens a socket to a remote port and receives a stream of data.
         The <url> has to be defined in CEng_python_lib.py in order to be used, follow
         the templates are written there.

 Usage:

 Command Line 1:  ./CEng_check_url.py <hostname> <url>

 Local Example:  ./CEng_check_url.py <hostname> <url>

 TODO:

'''

from datetime import datetime
import socket
import sys
import re
a = re.compile("[0-9]")

import CEng_python_lib as ceng_lib

# Check to see if commandline arguements were entered and if so
# attempt to validate them with regex's
if len(sys.argv)  != 4:
    print('Please enter a server, port,  and a url to check')
    sys.exit(2)
else:
    loc = sys.argv[3]
    if a.match(sys.argv[2]):
        port = int(sys.argv[2])
    else:
        print('Please enter a valid port number')
        sys.exit(2)
    server = ceng_lib.validate_hostname(sys.argv[1])
    if server:
        server = sys.argv[1]
    else:
        print('Please enter a valid server to connect to')
        sys.exit(2)

def main():

   # Execution start time
   start_time = datetime.now()

   # Open a socket to port a port
   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
       conn.connect((server, port))
   except IOError:
       print('There is no service listening on port 8080. Make sure the service is running and listening on port 8080')
       sys.exit(2)
   else:
       pass


   # Check for the desired output
   if loc == 'root':
       output = ceng_lib.get_port_output(conn)
       conn.close()

   elif loc == 'icinga-web':
       output = ceng_lib.get_icinga_http_output(conn)
       run_time = datetime.now() - start_time

   if output:
       print('%s; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (output, run_time))
       sys.exit(0)
   else:
       print('There is a problem with the service on the server; | \'Check_Time\'=%s;;;0.000000;60.000000;' % (run_time))
       sys.exit(2)


if __name__ == "__main__":
    main()
