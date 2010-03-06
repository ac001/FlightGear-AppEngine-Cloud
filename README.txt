This project started out as an Aircraft database, but it has also now
ended up with an idea for a new www.flightgear.org website.

Both these sites run on the Google App Engine.
http://code.google.com/appengine/

You can start developing by simply
* Taking a snapshot
* Enter the directory adn run ./run_local_server,sh
* Point you browser at http://localhost:8080
* NOTE: There will be not entities (ie data) in the "store"

==================================
-- FlightGear WWW Idea --
==================================
This site is under the /idea/ directory.


==================================
-- FlightGear Aircraft Database --
==================================

This is work in progress of an idea to host Flight Gear aircraft data on the Google AppEngine cloud.
http://fg-aircraft.appspot.com/
Its a mashup. Initial R+D. 

The idea is to create a database of FlightGears aircraft.

Intentions
* pull data from repositories and feeds

The code is available at git hub.
http://github.com/ac001/fg-aircraft

------------------
Structure
------------------
/google_appengine/
  is a copy  google code and included for convenience

run_local_server.sh
  running this script, sh ./run_local_server.sh starts and the tomcat local web server
  then visit the port http:://localhost:8080 after a few moments

/fg-aircraft/
  The code deployed to the google app engine at http://fg-aircraft.appspot.com

/scripts/
  Various Import scripts for local use and push pull to cloud and generally process data

/junk/
  NOT included
