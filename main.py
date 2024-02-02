from db_utils import RDSDatabaseConnector as RDSdbcon
from data_transform import DataTransform as Transformer
from dataframeinfo import DataFrameInfo 
import pandas as pd
import pandasgui as pdgui

if __name__ == '__main__':
    df = pd.read_csv("loan_payments.csv")
    # pdgui.show(df)
    
    #transformer = Transformer()
    
    #df = transformer.transform_employment_length(df)
    #df = transformer.cast_column_dtypes(df)
    df_info = DataFrameInfo(df)
    #print(df_info.column_statistics)
    null_counts = df_info.get_null_counts(show='True')
    print(null_counts)
    df_info.get_only_columns_with_nulls(show='True')
    #df_info.show_categorical_columns()
    #df_info.show_numerical_columns()
    #df_info.get_median()
    #df_info.get_percentiles()
    #df_info.get_counts()
    #print(df.head(10))
