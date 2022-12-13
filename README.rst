README
######


**NAME**


``JSONBOT`` - The JSON Everywhere Bot


**SYNOPSIS**


| ``jsonbot [-c] [-i] [-r]``
| ``jsonbot <cmd> [key=value] [key==value]``
|


**DESCRIPTION**


``JSONBOT`` is a bot, intended to be programmable, with a client program to
develop modules on and a systemd version with code included to run a 24/7
presence in a channel. 

``JSONBOT`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object. ``JSONBOT`` uses ~/.jsonbot/mod to read
modules from.


``JSONBOT`` has some functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.



**INSTALL**

|
| ``pip3 install jsonbot``
|

**CONFIGURATION**

|
| configuration is done by calling the ``cfg`` command of ``jsonbot``
| 

**irc**


| ``jsonbot cfg server=<server> channel=<channel> nick=<nick>``
|
| (*) default channel/server is #jsonbot on localhost
|

**sasl**


| ``jsonbot pwd <nickservnick> <nickservpass>``
| ``jsonbot cfg password=<outputfrompwd>``
|

**users**


| ``jsonbot cfg users=True``
| ``jsonbot met <userhost>``
|

**rss**


| ``jsonbot rss <url>``
|


**RUNNING**


this part shows how to run ``jsonbot``.

**cli**

without any arguments ``jsonbot`` doesn't respond, add arguments to have
``jsonbot`` execute a command:


| ``$ jsonbot``
| ``$``
|

the ``cmd`` command shows you a list of available commands:


| ``$ jsonbot cmd``
| ``cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,log,met,mre,nme,pwd,rem,rss,tdo,thr,ver``
|

**console**

use the -c option to start the bot as a console.


| ``$ jsonbot -c``
| ``JSONBOT started at Fri Sep 16 02:11:23 2022``
| ``> cfg``
| ``server=localhost port=6667 channel=#jsonbot nick=jsonbot cc=!``
| ``> thr``
| ``Console.loop(8s) IRC.keep(8s) IRC.loop(8s) IRC.output(8s) thr(8s) Fetcher.run/4m59s``
|

**COMMANDS**


here is a short description of the commands.


| ``cfg`` - show the irc configuration, also edits the config
| ``cmd`` - show all commands
| ``dlt`` - remove a user
| ``dne`` - flag todo as done
| ``dpl`` - set display items for a rss feed
| ``flt`` - show a list of bot registered to the bus
| ``fnd`` - allow you to display objects on the datastore, read-only json files on disk 
| ``ftc`` - run a rss feed fetching batch
| ``log`` - log some text
| ``met`` - add a users with there irc userhost
| ``mre`` - displays cached output, channel wise.
| ``nme`` - set name of a rss feed
| ``pwd`` - combine a nickserv name/password into a sasl password
| ``rem`` - remove a rss feed by matching is to its url
| ``rss`` - add a feed to fetch, fetcher runs every 5 minutes
| ``thr`` - show the running threads
| ``tdo`` - adds a todo item, no options returns list of todo's
| ``upt`` - show uptime
| ``ver`` - show version
|


**PROGRAMMING**


The ``jsb`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> from jsb import Object
>>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from jsb import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from jsb import Object, save
 >>> o = Object()
 >>> save(o)
 jsb.object.Object/89efa5fd7ad9497b96fdcb5f01477320/2022-11-21/17:20:12.221192


**SYSTEMD**


to run the bot after reboot, install the service file and start the service
by enabling it with ``--now``::


 $ ``sudo systemctl enable /usr/local/jsonbot/jsonbot.service --now

 (*) default channel/server is #jsonbot on localhost

 use ``jsonbotctl`` instead of the use ``jsonbot`` program

 $ ``sudo jsonbotctl cfg server=<server> channel=<channel> nick=<nick>``
 $ ``sudo jsonbotctl pwd <nickservnick> <nickservpass>``
 $ ``sudo jsonbotctl cfg password=<outputfrompwd>``
 $ ``sudo jsonbotctl cfg users=True``
 $ ``sudo jsonbotctl met <userhost>``
 $ ``sudo jsonbotctl rss <url>``


**AUTHOR**


Bart Thate - bthate@dds.nl


**COPYRIGHT**


``JSONBOT`` is placed in the Public Domain.
