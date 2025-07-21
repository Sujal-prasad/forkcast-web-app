import joblib 
import sklearn
import os
from utlils.search_location import search_location
from utlils.user_location import current_location_user


model_path = os.path.join("model", "final_model_file.pkl")
model = joblib.load(model_path)
if not os.path.exists(model_path):
    raise FileNotFoundError("Model file not found. Please train and save it first.")

def model_predict(distance_km, price_level, rating, total_reviews):
    return model.predict([[distance_km, price_level, rating, total_reviews]])






