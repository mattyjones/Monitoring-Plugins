Overview
========

There are various packages devoted to monitoring plugins out there and many are very good, there are downsides to most of them though.  This project means to try and fix some of those downsides.  This will be a collection of plugins ported from various other packages along with various scripts I and others have found useful.  They are written in Python and will give the user much more control over how the output is displayed and acted upon.

Goals
-----

The main goal is modular, clean Python code from which individual users can customize solutions to fit their needs. I am using Python instead of the more traditional C because the rapid development and lower entry bar far exceed the perceived benefits of C in a project like this.  I shouldn't have to recompile a plugin every time I need to make a change.  All scripts are being primarily written on Cent6 with Python 2.6, as best I can I am trying to achieve backwards compatibility to Python 2.4, which will allow Cent5 to run all code.  To this effect I have had to make some sacrifices, such as C style formating but I can live with that for now.

I have also tried to keep the package dependency list down, relying on the standard library as much as possible but in some cases it made more sense to install a library to do the heavy lifting than use subprocess to run a lot of shell/sed/awk commands, this would've defeated the purpose of using Python.

The other major goal of the project is to be a single place where user contributed scripts, service checks, and other debris can live.  The more people add to this collection here, the better it becomes.  They should include not just service checks, but notification scripts and scripts used to work with the configuration files.

Future Plans
------------

The creation of an rpm package is high on the list to make it simpler for people to install these.  This will be done using Python's bdist_rpm command so that users can tailor the rpm to their needs.  Many shops require rpm's for installation and they need to be built and signed locally.

I am also thinking about a gui.  My current thoughts on this are it will most likely be ncurses, as most people who don't already have a management tool will log into the monitoring servers over SSH.  I would like to avoid having to configure ssh for X, if it is even installed on a remote server, which is unlikely, so this seems like the next best idea at this point.  Web based is also a thought but this is a pipe dream at this point and will most likely be a entirely separate project.

Project Organization
====================

Notification Scripts
--------------------

The notification scripts folder currently contains an email script that I wrote and use that was loosely based upon a Perl script I inherited from a colleague who found it online.  I ported it to Python and converted it to use templates and css.  I have no idea of the original developer, if it's you, drop me a line and I will give credit.

This folder will be for any custom email scripts, html templates, or any other scripts or tools used to notify users or admins.

Management Scripts
------------------

The management scripts folder contains anything that manipulates the monitoring server itself or any configuration files, event handlers should also go here.

Service Checks
--------------

All service checks should be placed here.

Getting Started
==========

Installation
-----------

There are several ways to install these scripts, the easiest way would be to clone the repo. 

1. Clone the repository to a directory that has execute privileges by the necessary user
2. Install the necessary dependencies
3. Add the directory to your resources.cfg file
4. Add the service check command with the necessary arguments to your commands.cfg file
5. If necessary add the check command to your nrpe.cfg file
6. Add the new checks to any hosts you wish to monitor
7. Restart all necessary services

You can also download a zip file and unpack it to a directory that has execute privileges by the necessary user then follow the steps from there.

Usage
-----

The service checks all contain samples that can be added directly to your commands.cfg file. 

Features
--------

Each service check will have the ability to independently configure the exit code that tells the monitoring server what state it exited with. To get the desired results in the dashboard or notifications you can use the tables below.

| State      |  Value
| -----------|--------
|  OK        |  0
|  WARNING   |  1
|  CRITICAL  |  2
|  UNKNOWN   |  3


| --warning     | --critical    | WARNING Value  | CRITICAL Value
| ------------- |-------------  | -------------  | -------------
|   no          |   no          |   OK           |   OK
|   !no         |   no          |   WARNING      |   WARNING
|   no          |   !no         |   OK           |   CRITICAL
|   !no         |   !no         |   WARNING      |   CRITICAL

For example if I am deploying Icinga to a QA environment where nothing is critical then I would use _--critical no_ as an argument for the service check in the host configuration file.  This will set the _CRITICAL_ variable to _WARNING_.  If you were implementing some administration scripts and didn't want to have them alert ever but still want the monitoring server to execute them as checks, you would use _--warning no --critical no --unknown no_.  Now all exit code variables will point to _OK_.  If _unknown_ is set to 'no' it will point to _OK_.

How To Contribute
=================

Any sort of help is always welcome.  To get started clone the repo and start using it and submit feedback about what works and what needs fixing.  If you would like to add to the repo, then fork it, do your thing, and submit a pull request.  As long as the submission has some use to the monitoring community it is welcome.

For general questions on Python coding standards or how to write an effective commit message see the links below

+ [Python Coding Standards](http://legacy.python.org/dev/peps/pep-0008/)
+ [Writing effective commit messages](http://who-t.blogspot.de/2009/12/on-commit-messages.html)


