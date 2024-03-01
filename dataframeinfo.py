import pandas as pd

class DataFrameInfo:

    def __init__(self, df: pd.DataFrame):
        self.df = df
        # All numerical columns except the frist three
        # columns: (Unnamed), id and member_id
        column_statistics = self.df.describe()
        self.numerical_column_names = column_statistics.columns
        self.column_statistics = column_statistics.T
        

    def describe_column_dtypes(self) -> pd.DataFrame:
        column_dtypes = self.df.info(verbose=True, show_counts=False) 
        return column_dtypes
    
    def get_statistics(self) -> pd.DataFrame:
        all_stats = self.column_statistics
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
        numerical_columns_df = self.df[self.numerical_column_names]
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

    def list_categorical_columns(self, return_list = False):
        categorical_columns = [col for col in self.df.columns
                                    if col not in self.numerical_column_names][3:]
                                   # index list to skip (Unnamed), id and member_id
        if return_list:
            return categorical_columns
        else:
            value_counts = [len(self.df[col].unique()) for col in categorical_columns]
            category_columns_values_info = pd.DataFrame({'categorical column':categorical_columns,'number of unique values': value_counts})
            print(f"\n\nCategorical Columns and their Unique Values: \n{category_columns_values_info}")

    def list_numerical_columns(self, return_list = False):
        numerical_columns = [col for col in self.df.columns
                                    if col in self.numerical_column_names][3:]
        if return_list:
            return numerical_columns
        else:
            value_counts = [len(self.df[col].unique()) for col in numerical_columns]
            numerical_columns_values_info = pd.DataFrame({'categorical column':numerical_columns,'number of unique values': value_counts})
            print(f"\n\nNumerical Columns and their Unique Values: \n{numerical_columns_values_info}")

    def list_datetime_columns(self):
        datetime_columns = []
        for column in self.df.columns:
            if self.df[column].dtype == '<M8[ns]':
                datetime_columns.append(column)
        
        return datetime_columns 
