import pandas as pd
from sqlalchemy import create_engine
import os
import re

DATABASE_URL = "postgresql://user:password@localhost:5433/ames_housing"

def upload_raw_data():
    csv_path = "data/raw/AmesHousing.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    try:
        engine = create_engine(DATABASE_URL)
        df = pd.read_csv(csv_path)
        
        df.columns = [re.sub(r'[/ ]', '_', c.lower()) for c in df.columns]
        
        df.to_sql('raw_housing_data', engine, if_exists='replace', index=False, chunksize=500)
        
        print("Success: Data has been uploaded to the PostgreSQL database.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    upload_raw_data()