import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


training_data = pd.read_csv("C:\\Users\\sujal\\Downloads\\forkcast_dataset.csv")
model_dataframe = training_data.drop(["name"], axis=1)


model_dataframe["model_score"] = (
    -0.4 * model_dataframe["distance_km"]
    + 0.3 * np.log1p(model_dataframe["total_reviews"])
    + 0.1 * model_dataframe["price_level"]
    + 0.2 * model_dataframe["rating"]
)


x = model_dataframe[["rating", "price_level", "distance_km", "total_reviews"]]
y = model_dataframe["model_score"]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

n_estimators = [20, 60, 80, 100]
max_depth = [2, 8, None]
max_features = [0.2, 0.6, 0.8]
max_samples = [0.5, 0.75, 1.0]
parameter_grid = {
    'n_estimators': n_estimators,
    'max_depth': max_depth,
    'max_features': max_features,
    'max_samples': max_samples
}
grid_search = GridSearchCV(
    estimator=RandomForestRegressor(),
    param_grid=parameter_grid,
    cv=5,
    n_jobs=-1,
    verbose=2
)
grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print("Best CV score:", grid_search.best_score_)


final_model = RandomForestRegressor(
    n_estimators=100, max_depth=None, max_features=0.8, max_samples=1.0
)
final_model.fit(X_train, y_train)

print("Test set score:", final_model.score(X_test, y_test))
print("Train set score:", final_model.score(X_train, y_train))


def model_predict(rating, price_level, distance_km, total_reviews):
    return final_model.predict([[rating, price_level, distance_km, total_reviews]])


def recommend_random_restaurant(df=training_data, top_n=10):
    df = df.copy()
    df["model_score"] = (
        -0.4 * df["distance_km"]
        + 0.3 * np.log1p(df["total_reviews"])
        + 0.1 * df["price_level"]
        + 0.2 * df["rating"]
    )
    top_restaurants = df.sort_values(by="model_score", ascending=False).head(top_n)
    return top_restaurants.sample(1).to_dict(orient="records")[0]  

def get_trending_in_area(area_name, df=training_data):
    
    area_df = df[df["location"].str.contains(area_name, case=False, na=False)]

    if area_df.empty:
        return []

   
    area_df["model_score"] = (
        -0.4 * area_df["distance_km"]
        + 0.3 * np.log1p(area_df["total_reviews"])
        + 0.1 * area_df["price_level"]
        + 0.2 * area_df["rating"]
    )

    
    top_3 = area_df.sort_values(by="model_score", ascending=False).head(3)

   
    return top_3[["name", "location", "rating", "price_level", "total_reviews", "distance_km"]].to_dict(orient="records")
