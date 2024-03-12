import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from dataframeinfo import DataFrameInfo
from data_transform import DataTransform


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
    
    def detect_outliers_iqr(df, column):
        df_slice= df[[column]] 
        Q1 = df_slice[column].quantile(0.25)
        Q3 = df_slice[column].quantile(0.75)
        # Calculate IQR
        IQR = Q3 - Q1
        print(f"Q1 (25th percentile): {Q1}")
        print(f"Q3 (75th percentile): {Q3}")
        print(f"IQR: {IQR}")

        # Identify outliers
        outliers = df_slice[(df_slice[column] < (Q1 - 1.5 * IQR)) | (df_slice[column] > (Q3 + 1.5 * IQR))]
        print("Outliers:")
        outliers_not_nan = outliers[outliers[column].isna() == False]
        return outliers_not_nan
    
    def detect_outliers_zscore(df, column, num_std_dev = 'all'):
        # Testing z-score 
        df_slice= df[[column]] 
        mean = np.mean(df_slice[column])
        std_dev = np.std(df_slice[column])
        z_scores = (df_slice[column] - mean) / std_dev
        df_slice.loc[:,'z-score'] = z_scores
        if num_std_dev == 'all' or num_std_dev == 0:
            return df_slice
        elif num_std_dev > 0:
            positive_std_dev = df_slice[df_slice['z-score'] > num_std_dev] 
            return positive_std_dev
        elif num_std_dev < 0:
            negative_std_dev = df_slice[df_slice['z-score'] > num_std_dev] 
            return negative_std_dev
        else:
            raise "Invalid input for num_std_dev, please specify the number of standard_deviations to return"

    
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
    data_imputer = DataFrameTransform()
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
