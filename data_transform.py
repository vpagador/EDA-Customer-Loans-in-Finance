import pandas as pd
import pandasgui as pdgui
import numpy as np
import re
from yaml import load,SafeLoader
from sklearn.preprocessing import OrdinalEncoder


class DataTransform:
    

    def read_casting_map(self,filepath:str = 'cast_dtypes.yaml'):
        '''
        Opens the yaml file conataining the mapping 
        of each column to the desired datatype
        
        Parameters:
        -----------
            filepath: str
                yaml or json file
        '''
        with open(filepath) as f:
            cast_col_types = load(f, Loader=SafeLoader)
        return cast_col_types

    def transform_employment_length(self, df:pd.DataFrame):
        '''
        Extracts number value from employment_length column and casts to float
        
        Parameters:
        -----------
            df: pd.DataFrame
                Data set represented in pandas dataframe
        '''
        enc = OrdinalEncoder()
        X = df[['employment_length']]
        df[['employment_length']] = enc.fit_transform(X)  
   
        return df
    
    def cast_column_dtypes(self, df:pd.DataFrame):
        """
        Casts appropriate datatypes to every column in the dataset

        Parameters:
        -----------
            df: pd.DataFrame
                Data set represented in pandas dataframe
        """
        
        cast_col_types = self.read_casting_map()
        for col in cast_col_types.keys():
            print(f"{col} --> {cast_col_types[col]}")
            # Casts numerical types
            if  cast_col_types[col] in ['int32', 'float32']:
                try:
                    df[col] = df[col].astype(np.dtype(cast_col_types[col]))  
                except: 
                    df[col] = df[col].astype(np.dtype('float32'))
            # Casts datetypes
            elif cast_col_types[col] in ['date']:
                df[col] = df[col].apply(pd.to_datetime, format = 'mixed')
            # Casts otehr types like category
            else:
                df[col] = df[col].astype(cast_col_types[col])
            
        return df
