import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_tranformation import DataTransformation
from src.components.data_tranformation import DataTransformationConfig
from src.components.model_trainer import Model_Traineer_config
from src.components.model_trainer import Model_Trainer

@dataclass
class DataIngenstionConfig():
    train_data_path:str = os.path.join("artifact","train.csv")
    test_data_path:str = os.path.join("artifact","test.csv")
    raw_data_path:str = os.path.join("artifact","raw.csv")

class DataIngenstion:
    def __init__(self):
        self.ingestion_config = DataIngenstionConfig()

    def initiate_data_ingestion(self):
        logging.info("enter the data ingestion method or componets")
        try:
            df = pd.read_csv("notebook\data\stud.csv")  
            logging.info("Read The Dataset As DataFrame")  

            # os.mkdir(os.path.dirname(self.ingestion_config.train_data_path),exist_ok = True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index =False , header=True)

            logging.info("train-test-split-initiated!!!")
            train_set,test_set = train_test_split(df,random_state=42, test_size=0.2)

            train_set.to_csv(self.ingestion_config.train_data_path,index =False , header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index =False , header=True)

            logging.info("Ingenstion Of Code Is Completed!!!")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                
            )

        except Exception as e:
            raise CustomException(e,sys)
            

if __name__ == "__main__":
    obj=DataIngenstion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)
    modeltrainer  = Model_Trainer()
    score = modeltrainer.initiate_model_trainer(train_arr,test_arr)
    print(score)


            

