IPpy
====

Parallel testing of IP addresses and domains in python. Reads IP
addresses and domains from a CSV file and gives two lists of accessible
and inaccessible ones.

About
-----

-  Compatible with both Python 2 and 3.
-  Testing of IPs and domains is done in parallel.
-  By default there are 4 Workers.
-  All Workers work on an input Queue and a output Queue.

Modes
-----

-  verbose - if true, ping output will be displayed.
-  output - ``json`` or ``csv``

Support
-------

-  Windows, Linux and macOS are supported.
-  Supports both IPv4 and IPv6 IPs, and domain names.

   ::

       # Examples
       127.0.0.1
       ::1
       localhost

Install
-------

::

    $ pip install ippy

Usage
-----

::

    # Create IPpy instance
    ippy_obj = ippy.Ippy()

    # Set config - verbose, output, num_workers
    # verbose - True or False
    # output - csv or json
    ippy_obj.set_config(True, 'csv', 4)

    # Set Input File
    ippy_obj.set_file(file='ip_list.csv')

    # Run IPpy
    ippy_obj.run()

    # Get Results
    output = ippy_obj.result()
    print(output)

Tests
-----

To run the tests, first install tox

::

    $ pip install tox

then run tox from the project root directory.

::

    $ tox
