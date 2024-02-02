import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


class DataFrameTransform:

    @staticmethod
    def knn_imputer(df, column):
        imputer = KNNImputer(n_neighbors=2)
        df[column] = imputer.fit_transform(df[[column]])
        return df
    
    @staticmethod
    def average_imputer(df, column, average_mode = 'mean'):
        if average_mode == 'mean':
            df[column] = df[column].fillna(df[column].mean())
        elif average_mode == 'median':
            df[column] = df[column].fillna(df[column].mean())
        elif average_mode == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
            
        return df