import pandas as pd
import numpy as np
from yaml import load,SafeLoader
from sklearn.preprocessing import OrdinalEncoder
from scipy.stats import boxcox
from scipy.stats import yeojohnson
import numpy as np

import sys

sys.path.append('../csv_files')


class DataTransform:
    

    def read_casting_map(self,filepath:str = '../csv_files/cast_dtypes.yaml'):
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
    
    def apply_powertransformation(self, df:pd.DataFrame, column,transformation='log'):
            if transformation == 'log':
                log_array = df[column].map(lambda i: np.log(i) if i > 0 else 0)
                return log_array
            elif transformation =='boxcox':
                boxcox_array = df[column] +1
                boxcox_array = boxcox(boxcox_array)
                boxcox_array = pd.Series(boxcox_array[0])
                return boxcox_array
            elif transformation == 'yeojohnson':
                yeojohnson_array = df[column]
                yeojohnson_array = yeojohnson(yeojohnson_array)
                yeojohnson_array = pd.Series(yeojohnson_array[0])
                return yeojohnson_array
            else:
                pass

        
    def powertransform_columns_all_methods(self, df:pd.DataFrame,columns_to_transform:list):
        log_arrays = []
        boxcox_arrays = []
        yeojohnson_arrays = []
        for column in columns_to_transform:
            log_array = self.apply_powertransformation(df,column,'log')
            log_arrays.append(log_array)

            boxcox_array = self.apply_powertransformation(df,column,'boxcox')
            boxcox_arrays.append(boxcox_array)

            yeojohnson_array = self.apply_powertransformation(df,column,'yeojohnson')
            yeojohnson_arrays.append(yeojohnson_array)

        return log_arrays, boxcox_arrays, yeojohnson_arrays 
    
    def powertransform_compare_method_effectiveness(self, df:pd.DataFrame,columns_to_transform:list):
        log_arrays,boxcox_arrays, yeojohnson_arrays = self.powertransform_columns_all_methods()
        results =[]
        for column, log_array, boxcox_array, yeojohnson_array in zip(columns_to_transform,log_arrays,boxcox_arrays, yeojohnson_arrays): 
            log_skew = log_array.skew()
            boxcox_skew = boxcox_array.skew()
            yeojohnson_skew = yeojohnson_array.skew()
            skew_compare= dict.fromkeys(["Log Transform", "Boxcox Transform", "YeoJohnson Transform"])
            print("\n",column)
            print(f"Log Transform Skew:\t{log_skew}")
            print(f"Boxcox Transform Skew:\t{boxcox_skew}")
            print(f"Yeojohnson Transform Skew:\t{yeojohnson_skew}")
            skew_compare["Log Transform"] = abs(log_skew)
            skew_compare["Boxcox Transform"] = abs(boxcox_skew)
            skew_compare["YeoJohnson Transform"] = abs(yeojohnson_skew)
            key_max = min(skew_compare, key = skew_compare.get)  
            print("The key with the maximum value is: ", key_max)
            print(f"Original:\t\t\t{df[column].skew()}")

            results.append(key_max)
            return results

def apply_powertransformations(df):
    transformer = DataTransform()
    loan_amount_transformed = transformer.apply_powertransformation(df,'loan_amount',transformation='boxcox')
    funded_amount_transformed = transformer.apply_powertransformation(df,'funded_amount',transformation='yeojohnson')
    funded_amount_inv_transformed = transformer.apply_powertransformation(df,'funded_amount_inv',transformation='yeojohnson')
    int_rate_transformed = transformer.apply_powertransformation(df,'int_rate',transformation='yeojohnson')
    instalment_transformed = transformer.apply_powertransformation(df,'instalment',transformation='boxcox')
    
    df['loan_amount'] = loan_amount_transformed
    df['funded_amount'] = funded_amount_transformed
    df['funded_amount_inv'] = funded_amount_inv_transformed
    df['int_rate'] = int_rate_transformed
    df['instalment'] = instalment_transformed

    return df