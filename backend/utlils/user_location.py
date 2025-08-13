import requests
import urllib.parse

def current_location_user(address):
    encoded_address = urllib.parse.quote(address)
    api_key = "AlzaSyMp41IhmtA6FFbzmmhroi24_kZEN8W1vji"
    url = f"https://maps.gomaps.pro/maps/api/geocode/json?address={encoded_address}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["status"].lower() == "ok" and data["results"]:
        result = data["results"][0]
        location = result["geometry"]["location"]
        return {
            "latitude": location["lat"],
            "longitude": location["lng"],
            "placeID": result.get("place_id")
        }
    else:
        raise Exception("Failed to fetch geolocation")
