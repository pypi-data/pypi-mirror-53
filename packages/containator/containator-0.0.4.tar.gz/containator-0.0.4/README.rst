Containator
===========

Runs docker containers with pre-defined parameters. Define run-time parameters
in a configuration file to spawn containers easily.

**NOTE:** Containator was developed with Python 3.4, though it should run
on any Python 3.


Install & use
-------------

Install the package using::

   pip3 install containator

Edit config file to define your containers. A sample config file can be found
in the source distribution, or downloaded from the `source repository`_.

Either provide a config file path on the command line with ``-c`` argument or let
the application read config files at the following default locations. All locations are
tried in order and definitions from latter files override previous definitions.

- ``/etc/containator.conf``
- ``~/.config/containator.conf``
- ``~/.containator.conf``

After they are configured, individual containers are started by providing their
name on the command line, for example::

   containator firefox

.. _source repository: https://gitlab.com/beli-sk/containator/raw/master/containator.conf.example


Locations
---------

`Containator packages`_ are available from PyPI.

The `project page`_ is hosted on GitLab.com.

If you find something wrong or know of a missing feature, please
`create an issue`_ on the project page. If you find that inconvenient or have
some security concerns, you could also drop me a line at <code@beli.sk>.

.. _Containator packages: https://pypi.python.org/pypi/containator
.. _project page:         https://gitlab.com/beli-sk/containator
.. _create an issue:      https://gitlab.com/beli-sk/containator/issues


License
-------

Copyright 2015, 2019 Michal Belica <code@beli.sk>

::

    Containator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Containator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Containator.  If not, see < http://www.gnu.org/licenses/ >.

A copy of the license can be found in the ``LICENSE`` file in the
distribution.
