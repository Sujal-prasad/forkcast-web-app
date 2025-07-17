from flask import Flask, render_template, url_for, request, jsonify
import os
import pandas as pd
import numpy as np
import math
import joblib

from utlils.search_location import search_location
from utlils.user_location import current_location_user

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'model', 'final_model_file.pkl'))

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/ranking', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        try:
            current_address = request.form.get('current_address')
            search_query = request.form.get('search_query')

            user_loc = current_location_user(current_address)
            user_lat = user_loc["latitude"]
            user_lon = user_loc["longitude"]

            results = search_location(search_query)
            df = pd.DataFrame(results)
            df = df.dropna(subset=["rating", "price_level", "total_reviews"])

            df["distance_km"] = df.apply(
                lambda row: calculate_distance(user_lat, user_lon, row["latitude"], row["longitude"]), axis=1
            )

            df["model_score"] = model.predict(df[["distance_km", "rating", "price_level", "total_reviews"]])

            top_10 = df.sort_values(by="model_score", ascending=False).head(10)

            return render_template('ranking.html', results=top_10.to_dict(orient="records"))

        except Exception as e:
            return render_template("ranking.html", error=str(e), results=[])

    return render_template('ranking.html')

@app.route('/random')
def random():
    try:
        results = search_location("restaurant")
        df = pd.DataFrame(results)
        df = df.dropna(subset=["rating", "price_level", "total_reviews"])
        top_10 = df.sample(n=10)
        return render_template("random.html", results=top_10.to_dict(orient="records"))
    except Exception as e:
        return render_template("random.html", error=str(e), results=[])

@app.route('/trending')
def trending():
    try:
        results = search_location("trending restaurants")
        df = pd.DataFrame(results)
        df = df.dropna(subset=["rating", "price_level", "total_reviews"])
        top_10 = df.sort_values(by=["total_reviews", "rating"], ascending=[False, False]).head(10)
        return render_template("trending.html", results=top_10.to_dict(orient="records"))
    except Exception as e:
        return render_template("trending.html", error=str(e), results=[])

if __name__ == '__main__':
    app.run(debug=True)
