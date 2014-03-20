Overview
--------

This is an initial 0.1 release.  I know these work and I am using them personally but I am no Python or monitoring genuis so I am sure they are rough around the edges.  My plan is to continue to port the nagios-plugins that I use to Python and if necessary or needed add additional functionality to them or in some cases clean them up and make them more reliable.  I have seen issues with some of them using the status.dat file in a large environment >400 hosts and have moved them to use the REST API instead.  I am always open to suggestions or additions.

Goals
-----

The main goal is modular, clean Python code from which individual users can customize solutions to fit their needs.  I understand the performance and portability reasons for using C but I have seen no performace issues at all in very large environments, over 400 hosts/8000 checks on a single server using gearmon and nrpe.  The rapid development and lower entry bar far exceed the preceived benefits of C in a project like this.  All of these scripts will work with Python greater than 2.6, and many/most will work with Python 2.4, I am specifically using C style formating to maintain as much backwards compatability as possible even though I would much prefer to use the new format function.

The other major goal of the project is to be a single place where user contributed scripts, service checks, and other debris can live.  The more people add to the collection here, the better it becomes.  The should include not just service checks, but notification scripts, scripts used to add service checks, or work with the configuration files in other ways.

Notifications
-------------

The notifications folder is an email script that I wrote and use that was loosely based upon a Perl script I inherited from a colleague who found it online.  I ported it to Python and converted it to use templates and css.  I have no idea of the original developer, if it's you, drop me a line and I will give credit.

Management Scripts
------------------

The management folder is a currently a single script but in the future I will be porting my collection of sed/awk scripts to python.

Service Checks
--------------

This will contain all service checks.

Future Plans
------------

I would like to create an rpm package at some point to make it more simple for people to install these.  I will do this using Python's bdist_rpm command so that users can tailor the rpm to their needs.  I know many shops require rpm's for installation and they need to be built and signed locally so this will be high on my list.  

I am also thinking about a gui.  My thoughts on this are it will most likely be ncurses, as most people who don't already have a management tool will log into the Icinga servers over SSH.  I would like to avoid having to configure ssh for X, if it is even installed on a remote server which is unlikely, so this seems like the next best idea at this point.  Web based is also a thought but this is a pipe dream at this point and will most likely be a entirely seperate project.
