import pandas as pd
import numpy as np
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
    
    def extract_digit_from_string(self, string):
        '''
        Extracts number value from string
        '''
        try:
            digit =''
            for char in string:
                if char.isdigit():
                    digit = digit + char
            return digit
        except:
            pass
        
    
    def transform_digit_string(self, df:pd.DataFrame, column = 'term'):
        '''
        Convert string to int  
        
        Parameters:
        -----------
            df: pd.DataFrame
                Data set represented in pandas dataframe
        '''
        df[column] = df[column].apply(lambda x: self.extract_digit_from_string(x))

        return df

    def encode_transform(self, df:pd.DataFrame, column = 'employment_length'):
        '''
        Encodes employment_length column 
        
        Parameters:
        -----------
            df: pd.DataFrame
                Data set represented in pandas dataframe
        '''
        enc = OrdinalEncoder()
        X = df[[column]]
        df[[column]] = enc.fit_transform(X)
   
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
            # Casts other types like category
            else:
                df[col] = df[col].astype(cast_col_types[col])
            
        return df
