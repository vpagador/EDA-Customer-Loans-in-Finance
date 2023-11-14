from yaml import load, SafeLoader
from sqlalchemy import create_engine, inspect
import pandas as pd

class RDSDatabaseConnector:

    def __init__(self, creds_filepath):
        self.creds_filepath = creds_filepath
    
    def read_db_creds(self):
        with open(self.creds_filepath) as f:
            creds = load(f, Loader=SafeLoader)
        format_creds = (f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}"
        f"@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        return format_creds
    
    def init_db_engine(self, format_creds):
        engine = create_engine(format_creds).connect()
        print(engine)
        return engine
    
    def read_rds_table(self, engine):
        inspector = inspect(engine)
        table_list = inspector.get_table_names()
        table = table_list[0] 
        try:
            query = f"SELECT * from {table};"
            with engine as con:
                df = pd.read_sql_query(query, con=con)
            return df

        except Exception as err:
            print(f'Failed to read data')
            print(f'{err.__class__.__name__}: {err}')
            return pd.DataFrame()
    
    def export_to_csv(self, df):
        df.to_csv("loan_payments.csv")
     
        
if __name__ == '__main__':
    connector = RDSDatabaseConnector("credentials.yaml")
    creds = connector.read_db_creds()
    engine = connector.init_db_engine(creds)
    df = connector.read_rds_table(engine)
    connector.export_to_csv()