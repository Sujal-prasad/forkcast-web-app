import requests as r
import urllib.parse


def current_location_user(curr_address):
    address_encod=urllib.parse.quote(curr_address)
    url=f"https://maps.gomaps.pro/maps/api/geocode/json?key=AlzaSyDsozy2c6S85G-i3pvZI_17xxm90J4xzDU&address={address_encod}"
    response=r.get(url)
    location=response.json()
    if location["status"]=="ok" and len(location["results"])>0:
        location_result=location["results"][0]
        latitude=location_result["geometry"]["location"]["lat"]
        longitude=location_result["geometry"]["location"]["lng"]
        placeID=location_result["place_id"]
        return latitude,longitude,placeID
    else:
        raise Exception("failed to fetch data")
def main():
    try:
        lat,long,id=current_location_user(curr_address=None)
    except:
        raise Exception("failed to fetch latitude,longtitude,place id")
if __name__=="__main__":
    main()


       


    
   
