This is work in progress of an idea to host Flight Gear aircraft data on the Google AppEngine cloud.

http://fg-aircraft.appspot.com/

Its a mashup.

Initial R+D.

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
