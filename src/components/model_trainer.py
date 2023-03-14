import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from  dataclasses import dataclass
 # Modelling
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings

from src.logger import  logging
from src.exception import CustomException
import sys
from src.utils import save_object,evaluate_model
import os

@dataclass
class Model_Traineer_config:
    trained_model_path = os.path.join("artifact","model.pkl")

class Model_Trainer:

    def __init__(self):
        self.Model_Trainer_Path=Model_Traineer_config()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("Spliting training and test input data!!!")
            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
                
            )

            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
                }

            model_report:dict = evaluate_model(X_train= X_train,
                                            y_train = y_train ,
                                            X_test = X_test,
                                            y_test=y_test,
                                            models = models
                                            ) 
            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            #To get best score algo
            best_model_name = list(models.keys())[list(model_report.values()).index(best_model_score)
            ]   

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise  CustomException("No best Model founded")

            logging.info("Best found model on both training and testing dataset")  

            save_object(
                file_path=self.Model_Trainer_Path.trained_model_path,
                obj=best_model
            ) 

            predicted = best_model.predict(X_test)
            r2_squre = r2_score(y_test,predicted)

            return r2_squre

        except Exception as e :
            raise CustomException(e,sys)
               
            