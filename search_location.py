import requests as r
import urllib.parse
import pandas as pd

def search_location(location_given):
    search_encod=urllib.parse.quote(location_given)
    api_key="AlzaSyDsozy2c6S85G-i3pvZI_17xxm90J4xzDU"
    url=f"https://maps.gomaps.pro/maps/api/place/textsearch/json?query={search_encod}&key=api_key"
    result=r.get(url).json()
    if(result["status"]=="ok" and len(result["results"])>0):
        data_for_model=[]
        for item in result["results"]:
            data={
                "name": item.get("name", ""),
                "rating": item.get("rating", None),
                "business_status": item.get("business_status", ""),
                "latitude": item["geometry"]["location"]["lat"],
                "longitude": item["geometry"]["location"]["lng"],
                "place_id": item.get("place_id", ""),
                "price_level": item.get("price_level", None),
                "total_reviews": item.get("user_ratings_total", None),
                "opening_hours": item.get("opening_hours", {}).get("open_now", "Unknown"),
                "address":item.get("formatted_address", "")
            }
            data_for_model.append(data)

        df=pd.DataFrame(data_for_model)
        return df
    else:
        raise Exception("failed to fetch data")
    
def main():
    try:
        df=search_location(location_given=None)

    except:
        raise Exception("error in loading data into data frame")
if __name__=="main":
    main()


