import pandas as pd
import pandasgui as pdgui
import numpy as np
import re
from yaml import load,SafeLoader


class DataTransform:
    
    def transform_employment_length(self, df:pd.DataFrame):
            df.loc[:,'employment_length'] = (df.loc[:,'employment_length'].
                                            apply(lambda x: ''.join(char for char in str(x) if char.isdigit())))
            df.loc[:,'employment_length'] = df.loc[:,'employment_length'].apply(lambda x: np.NaN if x == '' else x)
            return df
    
    def cast_column_dtypes(self, df:pd.DataFrame):
        with open('cast_dtypes.yaml') as f:
            cast_col_types = load(f, Loader=SafeLoader)
        
        for col in cast_col_types.keys():
            print(col)
            if  cast_col_types[col] in ['int32', 'float32']:
                try:
                    df[col] = df[col].astype(np.dtype(cast_col_types[col]))  
                except: 
                    df[col] = df[col].astype(np.dtype('float32'))
            elif cast_col_types[col] in ['date']:
                df[col] = df[col].apply(pd.to_datetime, format = 'mixed')
            else:
                df[col] = df[col].astype(cast_col_types[col])
            print(f'changed--{cast_col_types[col]}')
            
        return df
