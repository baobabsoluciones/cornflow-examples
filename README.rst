gui/dance
==========

Installation
---------------

In Windows, you need to replace the "source ..." line by: `venv/Scripts/activate`.

Steps::

    cd cornflow-examples/python
    python3 -m venv venv
    source venv/bin/activate
    pip install gui/dance/requirements.txt

Launch
---------------------

To open the app, just do the following::

    source ven/bin/activate
    python gui/dance/app.py


How it works
---------------------

You need to provide a link to a cornflow server. Then, a username and a password. login or signup.

The flow is the following:

1. Browse and import some instance from `gui/dance/data`.
2. Login (or signup).
3. Send instance (and check te instance appears in the list).
4. Click in the instance and click on Solve instance.
5. Update instances.
6. Click in the instance again and see if the execution below is green.
7. Click in the green execution and click on Get results.
8. Click in Show solution to show the colored graph.
