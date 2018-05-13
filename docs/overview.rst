.. the basics

BI-Beacon Overview
==================

BI-Beacons use a RESTful API.

There is only one end-point: ``/<systemid>``.

This endpoint serves as the controlling mechanism for
*system* with ID `systemid`.

A complete endpoint URL may look something like this:

   ``https://beacon-api.abcbusiness.com/my-super-monitor``

Many Beacons may be configured to use the same systemid -
this is intentional, and means you can spread out several
Beacons that indicate the same thing.

E.g you may use this if you have many offices, or if you
want a Beacon both in the conference room and at the coffee
machine.
