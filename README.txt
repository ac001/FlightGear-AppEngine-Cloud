==================================
-- FlightGear Cloud Experiment --
==================================

This is an experiment and R+D towards using the Google App Engine for FlightGear.

The project currently consists of:

* http://fg-www.appspot.com      - Front end website
* http://fg-aircraft.appspot.com - Aircraft database website
* http://fg-online.appspot.com   - Multiplayer website
* http://fg-master.appspot.com   - Shared CDN experimantal stuff
* http://fg-cache.appspot.com    - Shared CDN experimantal stuff

-----------------------------
Run local server
-----------------------------
To run a  site locally in devel mode, from the directory this file is in run:

./google_appengine/dev_appserver.py SiteName

where SiteName is for example fg-www, then point your browser
as http://localhost:8080

-----------------------------
Upload Site
-----------------------------
The upload a site, you need developer access then execute

./google_appengine/appcfy.py update SiteName


-----------------------------
Notes
-----------------------------
* The code is by not clean and tidy as yet.
* The fg-master is definately research into using one server for shared
  logo and stylesheets etc, to check both loading times and the possibility
  of globally making changes eg a "logo of the day".

-----------------------------
Important
-----------------------------
Within app.yaml, please bump up the version number as digits;
do not use characters eg 2a-test. The docs say its
possible but this leads to unpredictable results for bitter experience.

-----------------------------
Development
-----------------------------cd ..
If you want to join in the fun then contact me
*  "ac0001" on the chat channel irc.flightgear.org#flightgear
* ac001 at daffodil dot uk dot com

Most Wanted = Graphic Designer
and any other mad ideas

There's more notes in notes.pete.txt
