
Manage Solaris Zones in Python
==============================

This project holds a python module with a ctypes wrapper around some Solaris
specific calls.

Module can be retrieved from [pypi](http://pypi.python.org/pypi/pyzone/) as 
well:

    easy_install/pip install pyzone

Some code snippets
==================

List zones
----------

    zones = zone.list_zones()
    for identifier in zones.keys():
        print zones[identifier]
        print zone.get_state(identifier)

Boot a zone
-----------

    zone.boot_zone(item)
    print zone.get_state(item)

Available functions
-------------------

  * list_zones
  * get_state
  * boot_zone
  * halt_zone
  * shutdown_zone
  * restart_zone
  * ready_zone
  * call_zone_adm

Note
----

Please note that some operations can take a while to complete.

(c) 2011 tmetsch