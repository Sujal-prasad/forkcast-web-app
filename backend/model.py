import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


training_data=pd.read_csv("C:\\Users\\sujal\Downloads\\forkcast_dataset.csv")

#model training begins..
model_dataframe=training_data.drop(["name"],axis=1)

model_dataframe["model_score"]=(-0.4*model_dataframe["distance_km"]+0.3*np.log1p(model_dataframe["total_reviews"])+0.1*model_dataframe["price_level"]+0.2*model_dataframe["rating"])
#model dataframe after score...
model_dataframe

random_forest=RandomForestRegressor()
x=model_dataframe[["rating","price_level","distance_km","total_reviews"]]
y=model_dataframe["model_score"]

X_test,X_train,y_test,y_train=train_test_split(x,y,test_size=0.2,random_state=42)

n_estimators=[20,60,80,100]
max_depth=[2,8,None]
max_features=[0.2,0.6,0.8]
max_samples=[0.5,0.75,1.0]
parameter_grid={
    'n_estimators':n_estimators,
    'max_depth':max_depth,
    'max_features':max_features,
    'max_samples':max_samples
}
grid_search=GridSearchCV(estimator=random_forest,param_grid=parameter_grid,cv=5,n_jobs=-1,verbose=2)
grid_search.fit(X_train,y_train)
print("best parameters are",grid_search.best_params_)
print("best score is",grid_search.best_score_)
final_model=RandomForestRegressor(n_estimators=100,max_depth=None,max_features=0.8,max_samples=1.0)
final_model.fit(X_train,y_train)
print(final_model.score(X_test,y_test))
print(final_model.score(X_train,y_train))

#making a utility function for prediction when this file is imported somewhere


final_model_file=joblib.dump(final_model,"final_model_file.pkl")