.. overview documentation page; not very specific or details,
   more on a business/idea level!

~~~~~~~~~~~~
Architecture
~~~~~~~~~~~~


::

:                      ##############                          ##########################  
:      https GET   +-->#State Server#<=====================----#Cloud controlling system#
:       polling--> |   ##############                      |   ##########################
:                  |           ^                           |  
:    Internet      |           |                           | <---- https POST requests 
:  -  -  -  -  -  -| -  -  -  -| -  -  -  -  -  -  -  -  - |-  -  -  -  -  -  -
:      LAN         |           |                           |        
:           #############   #############          ########################
:           #BI-Beacon 1    #BI-Beacon 2#          #LAN controlling system#
:           #############   #############          ########################


BI-Beacon 1 and 2
    This is either physical or virtual BI-Beacon devices, showing some state of something interesting to your business.

State Server
    This is the source of state for BI-Beacons.

Controlling system
	This is the user of the Beacons - where API calls originate.


Background
~~~~~~~~~~

The BI-Beacon architecture is fairly simple, however might need
some explanation anyway since it is not the simplest of possible
designs, and this is intentional.

So let's begin with the simplest possible design and work our
way from there.



Idea 1: direct cable connections
--------------------------------

If we want to control devices in our offices, the simplest possible
idea would be to connect them directly to our computers.

Indeed, this is possible with a BI-Beacon, using a USB data cable
connected to a wall-powered PC, but since it requires USB-serial
device drivers, and the right user/device permissions on the PC in
question, it is actually harder to do than the REST API over WiFi!

This method also has the drawback of limiting the location of
a Beacon to the vicinity of a PC. And, the software controlling
the Beacon need to be on that PC.


Idea 2: dynamic IP addresses
----------------------------

The next natural step after direct connection to a PC would be
over the local network - be it WiFi or an ethernet cable,
giving the device a local IP.

So why not use this method?

Well, the reason is corporate IT networks; it is a mess in general!

Getting a dynamic IP by connecting a device to the network is one
thing, DHCP is common enough today that it can be generally relied
upon, however, what then? If you want to communicate to the (local)
device not connected to the (local) network, you would need it's
dynamic IP address.

At home, you could just login to your router (at least if your tech
savvy enough!) and find the IP number of the newly connected device.

But at work, unless you're the IT admin of the place, that is strictly
out of the question, not only for "security reasons", but also because
the IT department has enough on their hands already! And getting them
to configure a device to have a static IP is just .. many weeks of delivery
time, time none of us have or want to put into getting a BI-Beacon up
and running.

A drawback of this method is also the 'local' part - we cannot
control a BI-Beacon unless we're on the same network. Forget about
controlling it from the cloud!


Idea 3: IoT to the rescue!
--------------------------

So, as odd as it sounds, it is actually easier to make the device
an internet-global device instead of a local (direct cable, or 
local network) device!

The trick is to have devices get their state from a non-corporate
server outside the building, via secure HTTPs requests.

This means, the devices can get their dynamic, local IP adresses
inside of your fine and dandy corporate network, and then you
adress them indirectly by communicating with the state server,
which reside on the public internet!

So what you do, as an integrator or user of BI-Beacons, is you
send off HTTPs requests to the state server - or API server if
you prefer - which saves the states, and serves the states
to Beacons asking what state to switch to.

It Just Works™! :)


