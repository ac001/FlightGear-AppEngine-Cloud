==================================
-- FlightGear Cloud Experiment --
==================================

This is an experiment, R&D towards usign the Google App Engine.

The project consists of:
* fg-www.appspot.com      - the front end website
* fg-aircraft.appspot.com - Aircraft database website
* fg-online.appspot.com   - Multiplayer website
* fg-master.appspot.com   - Shared stuff

To run the site in devel mode, from the directory this file is in run:
./google_appengine/dev_appserver.py _site_name_
where _site_name_ is for example fg-www, then point your browser
as http://localhost:8080

The upload a site, you need developer access then execute
./google_appengine/appcfy.py _site_name_

== Notes ==
The fg-master is definately research into using one server for shared
logo and stylesheets etc, to check both loading times and the possibility
of globally making changes eg a "logo of the day"

If you want to join in the fun then contact
pete = ac0001 on the chat channel irc.flightgear.org#flightgear

Wanted = Graphic Designer


