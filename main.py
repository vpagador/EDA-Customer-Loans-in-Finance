from db_utils import RDSDatabaseConnector as RDSdbcon
from data_transform import DataTransform as Transformer
import pandas as pd
import pandasgui as pdgui

if __name__ == '__main__':
    df = pd.read_csv("loan_payments.csv")
    # pdgui.show(df)
    
    transformer = Transformer()
    df = transformer.transform_employment_length(df)
    df = transformer.cast_column_dtypes(df)
    print(df.info())
    