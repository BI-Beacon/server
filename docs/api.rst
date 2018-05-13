.. loosely based on old cilamp.se API V1 page


API
===

BI-Beacons are controlled via a RESTful web AP, but only indirectly via a state server (see Architecture_). This means it is possible to control Beacons from any programming language that can make HTTPs POST requests.

You configure a Beacon to continuously copy the state of a certain
system identifier, or systemid for short. A systemid is made up of at
least one character. Allowed characters classes are small and big
english letters, digits, underscore and dash, or put in regex form:

        ``[a-zA-Z0-9_-]+``

A systemid can be up to 255 characters long.

Several Beacons may use the same system identifier; they will then
show the same state.

*Note:* The systemid can be viewed as the access key of the Beacon,
as it is all that is needed to control a device. So make sure you
only share the systemid with those persons and systems that should
be able to control the device. Do not store it publicly unless you
want anyone to be able to change the state of your Beacon.

If you want to add some security, randomize a string of at least 30
letters and numbers and use that as the system identifier.

A system can be in one of two states:

+---------+--------------------------------------------------------+
| State   |  Meaning                                               |
+=========+========================================================+
| static  | BI-Beacon will show a constant color                   |
+---------+--------------------------------------------------------+
| pulsing | BI-Beacons will pulse with a given speed and color     |
+---------+--------------------------------------------------------+

*Static colors* give the impression of state of a system or process,
e.g. on or off, ready or failed.

*Pulsing colors* give the impression of something happening, e.g.
something is building or being processed.

The meaning of colors and pulses is up to your imagination.

Change state
------------

:URL:       ``https://:beacon-server/:systemid/``

:Method:    POST

:Parameters:
    {
      **color:** color specification (format "#RRGGBB")

      **period:** length of pulse in milliseconds (optional, format integer)
    }

:beacon-server
    This is the hostname of the state server.

:systemid
    This is the system identifier you want to change the state of.

*Note*: the parameters should be transmitted as URL encoded Form Data,
i.e. the request header Content-Type should be
``application/x-www-form-urlencoded``.


Parameter examples
~~~~~~~~~~~~~~~~~~

:Purpose:   Set beacon to green
:Parameters:

::

    {
        color: "#00FF00"
    }

:Purpose:   Set beacon to red and pulse once per second
:Parameters:

::

    {
        color: "#FF0000"
        period: 1000
    }


Expected response
~~~~~~~~~~~~~~~~~

On success

:Code:              200
:Body:

::

    {"message": "':systemid' updated"}

On error

:Code:              400
:Body:

::

    {"message": "<error message>"}


Sample Curl Call
~~~~~~~~~~~~~~~~

The following will make a POST request to the BI-Beacon state server ``api.bi-beacon.se`` to change the state of the system identified by `testsystem` to green:

::

    curl -X POST -F "color=#00FF00" "https://api.bi-beacon.se/testsystem"

