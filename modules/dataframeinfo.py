import pandas as pd
import numpy as np

class DataFrameInfo:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_statistics = self.get_statistics().T
        # column_tuple_1: numerical_columns, non_numerical_columns
        column_tuple_1 = self.classify_into_numerical_non_numerical_columns()
        self.numerical_columns = column_tuple_1[0]
        self.non_numerical_columns = column_tuple_1[1]
        # column_tuple_2: datetime_columns, datetime_columns
        column_tuple_2 = self.classify_into_datetime_categorical_columns()
        self.datetime_columns = column_tuple_2[0]
        self.categorical_columns = column_tuple_2[1]

    def describe_column_dtypes(self) -> pd.DataFrame:
        column_dtypes = self.df.info(verbose=True, show_counts=False) 
        return column_dtypes
    
    def get_statistics(self) -> pd.DataFrame:
        all_stats = self.df.describe()
        return all_stats
    
    def get_mean(self):
        mean_column = self.column_statistics[['mean']]
        return mean_column

    def get_mean_std(self):
        mean_std_columns = self.column_statistics[['mean','std']]
        return mean_std_columns

    def get_median(self):
        median_column = self.column_statistics[['50%']]
        return median_column
    
    def get_percentiles(self):
        percentile_columns = self.column_statistics[['min',	'25%',	'50%',	'75%',	'max']]
        return percentile_columns
    
    def get_counts(self):
        column_value_counts = self.column_statistics[['count']].astype('int') 
        return column_value_counts

    def info_null_counts(self):
        numerical_columns_df = self.df[self.numerical_columns]
        null_counts = numerical_columns_df.isna().sum()
        total_value_count = numerical_columns_df.count() + null_counts
        percentage_null_counts = round((null_counts/total_value_count),4)*100
        percentage_non_null_counts = 100 - percentage_null_counts
        null_count_info = pd.concat([null_counts,percentage_null_counts, percentage_non_null_counts], axis = 1)
        null_count_info= null_count_info.rename(columns={' ':'column name',
                                                         0:'number of nulls',
                                                         1:'percentage of nulls',
                                                         2: 'percentage of non-nulls'})

        return null_count_info
    
    def get_null_counts(self):
        null_count_info = self.info_null_counts()
        return null_count_info

    def get_only_columns_with_nulls(self):
        null_count_info = self.get_null_counts()
        only_columns_with_nulls = null_count_info[null_count_info["number of nulls"]>0]
        return only_columns_with_nulls
    
    def get_only_columns_with_nulls_percentage(self):
        percentage_null_info = self.get_only_columns_with_nulls()
        percentage_null_info = percentage_null_info.T[1:]
        return percentage_null_info
    
    def list_columns_with_nulls(self):
        null_columns = self.get_only_columns_with_nulls()
        return null_columns.T.columns

    def classify_into_numerical_non_numerical_columns(self):
        numerical_columns = []
        non_numerical_columns = []

        for col in self.df.columns:
            if type(self.df[col][0]) in [np.int32, np.float32, np.int64, np.float64]:
                numerical_columns.append(col)
            else:
                non_numerical_columns.append(col)
        return numerical_columns, non_numerical_columns

    def classify_into_datetime_categorical_columns(self):
        self.non_numerical_columns
        datetime_columns = []
        categorical_columns = []
        for col in self.non_numerical_columns:
            try:
                is_column_datetime = self.df[col][0:1].apply(pd.to_datetime, format = 'mixed')
                if type(is_column_datetime[0]) == pd._libs.tslibs.timestamps.Timestamp:
                    datetime_columns.append(col)
            except:
                categorical_columns.append(col)
                pass
        return datetime_columns, categorical_columns


if __name__=='__main__':
    df = pd.read_csv("loan_payments.csv")
    df_info = DataFrameInfo(df)
    print(df_info.numerical_columns)
    print(df_info.get_statistics())