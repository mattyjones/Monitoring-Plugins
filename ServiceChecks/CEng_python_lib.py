'''
Caffeinated Engineering Python Function Library
Matt Jones caffeinatedengineering@gmail.com
Created 10.21.13
Last Update 04.01.14

'''

import socket
import sys
import re

ok_status_exit_code = 0
warning_status_exit_code = 1
critical_status_exit_code = 2
unknown_status_exit_code = 3


def get_local_hostname():
    '''
        get_local_hostname
        takes: nothing
        returns: the hostname
        function: get the hostname

        This will get the FQDN and then split it at the first domain.  This
        will work will both RHEL5 and RHEL6.
    '''

    machine_name = socket.gethostname()
    machine_name = machine_name.split('.')
    return machine_name[0]

def validate_hostname(hostname):
    '''
        validate_hostname
        takes: a hostname or ip
        returns: a valid hoistname or ip
        function: to make sure a hostname or ip is valid

        This will take the hostanme or ip entered by the user and make sure it is valid
        before trying to use it.  Other checks can be added to include tld checking,
        but for now this is generic enough that it will apply across the board for most
        cases.

    '''
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def get_icinga_http_output(conn):
    '''
        get_icinga_output
        takes: a connection token
        returns a string
        function: search the output stream for a string and return it

        This will read the outpur stream from a get request to the icinga-web home
        page.  The first find will get the index of where I want to start reading and
        the second find will get the index of where I want to stop reading, then I
        remove the newline and return the string, which will be the webserver, version,
        and OS.

    '''

    conn.send('GET /icinga-web/ + \r\n\r\n')
    size = 128 # The size of the stream to receive
    r = conn.recv(size)
    x = r.find('Server:') # The start of the string I want
    if not x:
        print('There is a problem with the https server')
        sys.exit(2)
    y = r.find('X-') # The end of the string I want
    output = r[x:y]  # The string I want
    output = output.rstrip()
    return output

def get_port_output(conn):
    '''
        get_port_output
        takes: a connection token
        returns a string
        function: search the output stream for a string and return it

        This will read the outpur stream from a get request to the icinga-web home
        page.  The first find will get the index of where I want to start reading and
        the second find will get the index of where I want to stop reading, then I
        remove the newline and return the string, which will be the webserver, version,
        and OS.

    '''

    conn.send('GET / + \r\n\r\n')
    size = 128 # The size of the stream to receive
    r = conn.recv(size)
    x = r.find('Server:') # The start of the string I want
    if not x:
        print('There is a problem with the http server')
        sys.exit(2)
    y = r.find('X-') # The end of the string I want
    output = r[x:y]  # The string I want
    output = output.rstrip()
    #output = r
    return output
