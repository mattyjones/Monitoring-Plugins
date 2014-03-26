Overview
========

This is an initial 0.1 release.  I know these work and I am using them personally but I am no Python or monitoring genius so I am sure they are rough around the edges.  My plan is to continue to port the nagios-plugins that I use to Python and if necessary or needed add additional functionality to them or in some cases clean them up and make them more reliable.  I have seen issues with some of them using the status.dat file in a large environment >400 hosts and have moved them to use the REST API instead.  In the near future I will be using LiveStatus so that I can move away from any software dependencies.  I am always open to suggestions or additions.

Goals
-----

The main goal is modular, clean Python code from which individual users can customize solutions to fit their needs.  I understand the performance and portability reasons for using C but I have seen no performance issues at all in very large environments, over 400 hosts/8000 checks on a moderately provisioned single server using gearmon and nrpe.  The rapid development and lower entry bar far exceed the perceived benefits of C in a project like this.  All of these scripts will work with Python greater than 2.6, and many/most will work with Python 2.4, I am specifically using C style formating to maintain as much backwards compatibility as possible even though I would much prefer to use the new format function.

The other major goal of the project is to be a single place where user contributed scripts, service checks, and other debris can live.  The more people add to the collection here, the better it becomes.  The should include not just service checks, but notification scripts, scripts used to add service checks, or work with the configuration files in other ways.

Future Plans
------------

I would like to create an rpm package at some point to make it simpler for people to install these.  I will do this using Python's bdist_rpm command so that users can tailor the rpm to their needs.  I know many shops require rpm's for installation and they need to be built and signed locally so this will be high on my list.

I am also thinking about a gui.  My current thoughts on this are it will most likely be ncurses, as most people who don't already have a management tool will log into the Icinga servers over SSH.  I would like to avoid having to configure ssh for X, if it is even installed on a remote server, which is unlikely, so this seems like the next best idea at this point.  Web based is also a thought but this is a pipe dream at this point and will most likely be a entirely separate project.

Project Organization
====================

Notification Scripts
--------------------

The notification scripts folder currently contains an email script that I wrote and use that was loosely based upon a Perl script I inherited from a colleague who found it online.  I ported it to Python and converted it to use templates and css.  I have no idea of the original developer, if it's you, drop me a line and I will give credit.

This folder will be for any custom email scripts, html templates, or any other scripts or tools used to notify people concerning Icinga.

Management Scripts
------------------

The management scripts folder is a currently a single script but in the future I will be porting my collection of sed/awk scripts to python.  Anything that manipulates Icinga itself or any configuration files should go here.

Service Checks
--------------

This will contain all service checks.

How To Contribute
=================

Any sort of help is always welcome.  To get started clone the repo and start using the plugins and submit feedback about what works and what needs fixing.  If you would like to add the the repo, then fork it, do your thing, and submit a pull request.  As long as the submission has some use to the Icinga community specifically or the monitoring community as a whole, it is welcome.

