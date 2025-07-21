import requests
import urllib.parse

def search_location(query="restaurant"):
    encoded_query = urllib.parse.quote(query)
    api_key = "AlzaSyDsozy2c6S85G-i3pvZI_17xxm90J4xzDU"
    url = f"https://maps.gomaps.pro/maps/api/place/textsearch/json?query={encoded_query}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["status"].lower() == "ok" and data["results"]:
        restaurants = []

        for place in data["results"]:
            location = place.get("geometry", {}).get("location", {})
            restaurant = {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "latitude": location.get("lat"),
                "longitude": location.get("lng"),
                "place_id": place.get("place_id"),
                "price_level": place.get("price_level", 2),
            }
            restaurants.append(restaurant)

        return restaurants
    else:
        raise Exception("No results found or invalid API response")
