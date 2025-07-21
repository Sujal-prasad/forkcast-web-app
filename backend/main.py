from flask import Flask, render_template, request, jsonify
import os
import math
from joblib import load
import random

from utlils.search_location import search_location
from utlils.user_location import current_location_user

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

model = load(os.path.join(os.path.dirname(__file__), '..', 'model', 'final_model_file.pkl'))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/ranking')
def recommendation():
    return render_template('ranking.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/random')
def random_restaurant():
    return render_template('random.html')

@app.route('/trending')
def trending():
    return render_template("trending.html")

@app.route('/process-address', methods=['POST'])
def process_address():
    user_data = request.get_json()
    address = user_data.get("address")
    if not address:
        return jsonify({"error": "Address not found"}), 400
    try:
        result = current_location_user(address)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    user_area = data.get("user_area")
    restaurant_area = data.get("restaurant_area")

    if not user_area or not restaurant_area:
        return jsonify({"error": "Both user and restaurant areas are required."}), 400

    try:
        user_loc = current_location_user(user_area)
        restaurant_list = search_location(restaurant_area)
        ranked_restaurants = []

        for res in restaurant_list:
            if res['latitude'] and res['longitude']:
              
                res['name'] = res.get('name') or "Unnamed Restaurant"
                res['rating'] = res.get('rating') or 0
                res['price_level'] = res.get('price_level') or 1
                res['user_ratings_total'] = res.get('user_ratings_total') or 0

                distance = haversine_distance(
                    user_loc['latitude'], user_loc['longitude'],
                    res['latitude'], res['longitude']
                )

                features = [[
                    res['rating'],
                    res['price_level'],
                    distance,
                    res['user_ratings_total']
                ]]

                res['score'] = model.predict(features)[0]
                res['distance'] = round(distance, 2)
                ranked_restaurants.append(res)

        ranked_restaurants.sort(key=lambda x: x['score'], reverse=True)
        return jsonify(ranked_restaurants), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/random-restaurant', methods=['POST'])
def random_ranked_restaurant():
    data = request.get_json()
    user_area = data.get("user_area")
    restaurant_area = data.get("restaurant_area")

    if not user_area or not restaurant_area:
        return jsonify({"error": "Both locations are required."}), 400

    try:
        user_loc = current_location_user(user_area)
        restaurant_list = search_location(restaurant_area)
        top_restaurants = []

        for res in restaurant_list:
            if res['latitude'] and res['longitude']:
               
                res['name'] = res.get('name') or "Unnamed Restaurant"
                res['rating'] = res.get('rating') or 0
                res['price_level'] = res.get('price_level') or 1
                res['user_ratings_total'] = res.get('user_ratings_total') or 0

                dist = haversine_distance(
                    user_loc['latitude'], user_loc['longitude'],
                    res['latitude'], res['longitude']
                )

                features = [[
                    res['rating'],
                    res['price_level'],
                    dist,
                    res['user_ratings_total']
                ]]

                res['score'] = model.predict(features)[0]
                res['distance'] = round(dist, 2)
                top_restaurants.append(res)

        top_restaurants.sort(key=lambda x: x['score'], reverse=True)
        top_10 = top_restaurants[:10]
        random_choice = random.choice(top_10)
        return jsonify(random_choice), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trending-restaurants', methods=['POST'])
def trending_restaurants():
    data = request.get_json()
    user_area = data.get("user_area")
    restaurant_area = data.get("restaurant_area")

    if not user_area or not restaurant_area:
        return jsonify({"error": "Both user and restaurant areas are required."}), 400

    try:
        user_loc = current_location_user(user_area)
        restaurant_list = search_location(restaurant_area)
        trending = []

        for res in restaurant_list:
            if res['latitude'] and res['longitude']:
              
                res['name'] = res.get('name') or "Unnamed Restaurant"
                res['rating'] = res.get('rating') or 0
                res['price_level'] = res.get('price_level') or 1
                res['user_ratings_total'] = res.get('user_ratings_total') or 0

                dist = haversine_distance(
                    user_loc['latitude'], user_loc['longitude'],
                    res['latitude'], res['longitude']
                )

                features = [[
                    res['rating'],
                    res['price_level'],
                    dist,
                    res['user_ratings_total']
                ]]

                res['score'] = model.predict(features)[0]
                res['distance'] = round(dist, 2)
                trending.append(res)

        trending.sort(key=lambda x: x['score'], reverse=True)
        top_3 = trending[:3]

        return jsonify(top_3), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == '__main__':
    app.run(debug=True)
