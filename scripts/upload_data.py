import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def upload_data_to_render():
    file_path = 'data/raw/AmesHousing.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    df = pd.read_csv(file_path)

    EXTERNAL_URL = "postgresql://ames_housing_db_user:gXkOWtEA2cu389Vczp2LABNB7r3RBzC4@dpg-d799qk75r7bs73fns49g-a.oregon-postgres.render.com/ames_housing_db"

    if EXTERNAL_URL.startswith("postgres://"):
        EXTERNAL_URL = EXTERNAL_URL.replace("postgres://", "postgresql://", 1)

    try:
        engine = create_engine(EXTERNAL_URL)

        df.to_sql('ames_housing', engine, if_exists='replace', index=False)
        
        print("Success: Data has been successfully uploaded to the Render cloud database!")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

if __name__ == "__main__":
    upload_data_to_render()