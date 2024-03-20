import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from modules.dataframeinfo import DataFrameInfo
from modules.data_transform import DataTransform


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
    
    @staticmethod
    def detect_outliers_iqr(df, column, 
                            show_general_outlier_info =True, 
                            show_top_bottom_outliers = True):
        # Testing IQR for outliers 
        column_copy_df = df[[column]]

        MIN = column_copy_df.quantile(0)[0]
        Q1 = column_copy_df.quantile(0.25)[0]
        Q2 = column_copy_df.quantile(0.5)[0]
        Q3 = column_copy_df.quantile(0.75)[0]
        MAX = column_copy_df.quantile(1)[0]

        # Calculate IQR
        IQR = Q3 - Q1

        # Identify outliers
        bottom_test = Q1 - 1.5 * IQR
        top_test = Q3 + 1.5 * IQR
        outliers = column_copy_df[(column_copy_df < bottom_test) | (column_copy_df > top_test)]
        outliers_df = outliers[outliers[column].isna() == False]
        print(f"Bottom Value for Outliers: {bottom_test}")
        print(f"Top Value for Outliers: {top_test}\n")
        if show_general_outlier_info == True:
            print(f"IQR (Range): {IQR}")
            print(f"Q1: {Q1}")
            print(f"Q2: {Q2}")
            print(f"Q3: {Q3}\n")
            print(f"Minimum: {MIN}")
            print(f"Maximum: {MAX}\n")
            print(f"Outliers: \n {outliers_df}")
            print(f"Number of Outliers: {len(outliers_df)}\n")
        # Identify top and bottom outliers
        if show_top_bottom_outliers == True:
            outliers_bottom = outliers_df[outliers_df[column] < bottom_test]
            outliers_top = outliers_df[outliers_df[column] > top_test]
            print(f"Bottom Outliers: \n {outliers_bottom}")
            print(f"Number of Bottom Outliers: {len(outliers_bottom)}\n")
            print(f"Top Outliers: \n {outliers_top}")
            print(f"Number of Top Outliers: {len(outliers_top)}")

    @staticmethod
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

def drop_outliers(df):
    drop_conditions = ((df['annual_inc']<1000000) 
                        & (df['inq_last_6mths'] < 7) 
                        & (df['open_accounts'] < 30)  
                        & (df['total_rec_late_fee'] < 100)
                        & (df['recoveries'] < 10000)
                        & (df['collection_recovery_fee'] < 32)
                        & (df['collections_12_mths_ex_med'] == 0))
    df = df[drop_conditions]
    return df


if __name__ == '__main__':
    df = pd.read_csv('loan_payments.csv')
    transformer = DataTransform()
    df = transformer.encode_transform(df)
    df = transformer.transform_digit_string(df)
    df = transformer.cast_column_dtypes(df)
    df = impute_all_null_columns(df)
