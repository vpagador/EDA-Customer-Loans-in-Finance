import pandas as pd
import pandasgui as pdgui


class DataTransform:
    
    def explore_columns(self,df:pd.DataFrame):
        return df.info()

    def cast_column_dtypes(self, df):
        column_list = df.columns
        dtype_list = []
        cast_column_dict = {}
        for key, value in zip(column_list + 1, dtype_list):
            cast_column_dict[key] = value
        df.astype(cast_column_dict)

