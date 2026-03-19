This Flask app uses Open Street Map and ADSB.lol APIs to display the nearby flights within a certain radius of a given location.
This app works like the below:
(User Inputted Location) --> [App] --> {OpenStreetMap] --> [App] --> [ADSB.lol] --> [App]


(User gives location)
(App sends request to open street map for location, receives latitude and longitude)
(App sends request for ADSB data within 50 nautical miles of the given lat/long)
(App displays this on the html page)
