from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

#Assign variables for Form Data
def AssignVariables():
    address = request.form["address"]
    lat, lon = get_lat_long(address)
    planes = get_planes(lat, lon)
    return render_template("index.html", planes=planes, address=address)

#Make Index available at /
@app.route("/", methods=["GET", "POST"])
def index():
     if request.method == "POST":
          address = request.form["address"]
          lat, lon = get_lat_long(address)
          #DEBUGLINEBELOW
          print(f"DEBUG: Address submitted: '{address}', lat: {lat}, lon: {lon}")
          planes = get_planes(lat,lon)
          return render_template("index.html", planes = planes, address = address)
     return render_template("index.html", planes=[])

#Get Lat and Long from Address
def get_lat_long(address):
     response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": address,
            "format": "json",
            "limit": 1
        },
        headers={
            "User-Agent": "planes-overhead-app"
        }
    ) 
     data = response.json()
     if not data:
          return None, None
     return float(data[0]["lat"]), float(data[0]["lon"])

def get_planes(lat, lon):
    response = requests.get(f"https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/50")
    data = response.json()
    planes = []
    for plane in data["ac"]:
        flight = plane.get("flight", "").strip()
        altitude = plane.get("alt_baro")
        on_ground = plane.get("on_ground")

        if flight and isinstance(altitude, (int, float)) and altitude > 0 and on_ground is not True:
            planes.append({
                "flight": flight,
                "altitude": altitude,
                "type": plane.get("t"),
                "speed": plane.get("gs"),
                "distance": plane.get("dst"),
            })
    return planes


#Run App
if __name__ == "__main__":
        app.run(host="127.0.0.1", port = 5050, debug=True, use_reloader=True)