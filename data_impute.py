import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from dataframeinfo import DataFrameInfo
from data_transform import DataTransform


class DataImpute:

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
    
def impute_and_check(func):
    def wrapper(df):
        df_info = DataFrameInfo(df)
        only_columns_with_nulls = df_info.get_only_columns_with_nulls()
        print(only_columns_with_nulls)
        print("\nImputing null columns ....\n ")
        df = func(df)
        df_info = DataFrameInfo(df)
        only_columns_with_nulls = df_info.get_only_columns_with_nulls()
        print(only_columns_with_nulls)
        return df
    return wrapper

@impute_and_check
def impute_all_null_columns(df):
    data_imputer = DataImpute()
    df = data_imputer.average_imputer(df,'funded_amount','median')
    df = data_imputer.average_imputer(df,'term','mode')
    df['last_payment_date'] = df['last_payment_date'].fillna(df['last_payment_date'].median())
    df['last_credit_pull_date'] = df['last_credit_pull_date'].fillna(df['last_credit_pull_date'].median())
    df['collections_12_mths_ex_med'] = df['collections_12_mths_ex_med'].fillna(df['collections_12_mths_ex_med'].mode()[0])
    df = data_imputer.average_imputer(df,'int_rate','mean')
    df = data_imputer.knn_imputer(df,'employment_length')
    df = df.drop(columns=['mths_since_last_delinq','mths_since_last_record','next_payment_date','mths_since_last_major_derog'])
    return df


if __name__ == '__main__':
    df = pd.read_csv('loan_payments.csv')
    transformer = DataTransform()
    df = transformer.encode_transform(df)
    df = transformer.transform_digit_string(df)
    df = transformer.cast_column_dtypes(df)
    df = impute_all_null_columns(df)
