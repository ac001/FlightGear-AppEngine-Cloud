This is work in progress of an idea to host Flight Gear aircraft data on the Google AppEngine cloud.

Initial R+D.

The code is available at git hub.

If you want to hack then.

1) Goto git hub, and clone the snapshot 
  * its assumed u got python installed and git.
  * the google appengine is included in the snapshot.
  * Clone to your directory.

------------------
Structure
------------------
/google_appengine/
  is a copy of tested google code and included for convenience

run_local_server.sh
  running this script, sh ./run_local_server.sh starts and the tomcat local web server
  then visit the port http:://localhost:8080 after a few moments

/fg_aircraft_appspot/
  The code deployed to the google app engine at http://fg-aircraft.appspot.com

/scripts/
  Various Import scripts for local use and push pull to cloud and generally process data

/etc/
  Genernal docs and suoerfilous that needs to be shared
