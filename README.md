Overview
--------

This is an initial 0.1 release.  I know these work and I am using them personally but I am no Python or monitoring genuis so I am sure they are rough around the edges.  My plan is to continue to port the nagios-plugins that I use to Python and if necessary or needed add extra functionality to them or in some cases clean them up and make them more reliable.  I have seen issues with some of them using the status.dat file in a large environment >400 hosts and have moved them to use the REST API instead.  I am always open to suggestions or additions.

Goals
-----

The main goal is modular, clean code from which individual users can customize solutions to fit their needs.  I understand the performance and portability reasons for using C but I have seen no performace issues at all in very large environments, over 400 hosts/8000 checks on a single server using gearmon and nrpe.  All of these scripts will work with Python greater than 2.6, and many/most will work with Python 2.4, I am specifically using C style formating even though I would much prefer to use the new format function.  I would also like to build this into a single place where user contributed scripts, service checks, and other debris can live.  The more people add to the collection here, the better it becomes.

Notifications
-------------

The notifications folder is an email script that I wrote and use that was loosely based upon a Perl script I inherited from a colleague who found it online.  I ported it to Python and converted it to use templates and css.  I have no idea of the original developer, if it's you, drop me a line and I will give credit.

Management Scripts
------------------

The management folder is a currently a single script but in the future I will be porting my collection of sed/awk scripts to python with the ultimate goal of creating a simple configuration tool in python most likely using tk or ncurses.  It will be commandline driven, not a gui app requiring a desktop installation.  I may also think about a web interface using cgi scripts.

Future Plans
------------

I would like to create an rpm package at some point to make it more simple for people to install these.  I will do this using Python's bdist_rpm command so that users can tailor the rpm to their needs.  I know many shops require rpm's for installation and they need to be built and signed locally so this will be high on my list.  I may also compile the code to C using Cython for the benifit of portability, just a thought at this time though.
