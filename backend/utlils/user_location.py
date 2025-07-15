import requests as r
import urllib.parse

def current_location_user(address):
    address_encod = urllib.parse.quote(address)
    api_key = "AlzaSyDsozy2c6S85G-i3pvZI_17xxm90J4xzDU"
    url = f"https://maps.gomaps.pro/maps/api/geocode/json?key={api_key}&address={address_encod}"

    response = r.get(url)
    location = response.json()

    if location["status"] == "ok" and len(location["results"]) > 0:
        location_result = location["results"][0]
        latitude = location_result["geometry"]["location"]["lat"]
        longitude = location_result["geometry"]["location"]["lng"]
        place_id = location_result["place_id"]

        return {
            "latitude": latitude,
            "longitude": longitude,
            "placeID": place_id
        }
    else:
        raise Exception("Failed to fetch data from Geocoding API")


def main():
    try:
        result = current_location_user("Noida Sector 128")
        print(result)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
