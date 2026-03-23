Ames Housing Price Prediction Project

This project predicts house prices in Ames, Iowa, using regression models. I created a full pipeline that includes data cleaning and processing. Finally, I deployed the model using a FastAPI interface so it can provide real-time predictions.


Project Structure

I tried to keep everything organized. Here is how the folders look:

app/: This is where my FastAPI code lives. main.py runs the server and schemas.py checks if the input data is correct.
data/: I have raw data here. I also have a folder for processed data for later.
models/: After training, I saved my model and preprocessor here as .joblib files.
notebooks/: This is my "laboratory". I have 6 different notebooks for EDA, cleaning, and training.
sql/: I used some SQL to clean the initial data.
Dockerfile: To run this project easily anywhere using Docker.


How I Built It (The Workflow)

1.Data Cleaning & EDA

First, I connected to a PostgreSQL database to get the data. I found some missing values in garages and basements.

For numbers, I filled missing parts with 0.
For text, I used 'None'.
I also found a strange house: it was huge but the price was very low (an outlier!), so I deleted it.


2.Feature Engineering

I created some new features to help the model:

house_age: How old the house is when it was sold.
total_living_area: Combined first floor, second floor, and basement area.
total_bathrooms: Added full and half baths together.

I used Log Transform on the price and area columns because the numbers were too big and skewed.


3.Machine Learning

I used CatBoost (and tested others) to train the model. I split the data into 80% for training and 20% for testing.


4.Model Selection

I tested several models like XGBoost, LightGBM, and CatBoost.

The Overfitting Challenge:
Initially, most models (especially LightGBM and XGBoost) were overfitting. They had very high training scores but didn't perform as well on cross-validation.

Why I chose CatBoost:
Instead of fixing every model, I decided to focus on CatBoost. I tuned its parameters to reduce overfitting. As you can see in the table below, CatBoost now has a very small Gap (0.032) between Train and CV scores. This means the model is more reliable and will work better with new, unseen house data.

Model	Train R2	CV R2 Mean	Gap
LightGBM	0.998	0.903	0.095
CatBoost	0.931	0.898	0.032
Ridge	0.933	0.896	0.036
XGBoost	0.999	0.890	0.108

Why CatBoost? Even though LightGBM had a slightly higher CV score, CatBoost showed the best generalization. The Gap between Train and CV is very small (0.032), meaning the model is not overfitting.


5.API Usage (Example)

Once the server is running, you can test it via Swagger UI.

Request body

{
  "total_living_area": 1800.0,
  "overall_qual": 7,
  "gr_liv_area": 1200.0,
  "exter_qual": 4.0,
  "kitchen_qual": 4.0,
  "total_bathrooms": 2.0,
  "year_built": 2010,
  "bsmt_qual": 4.0,
  "house_age": 16,
  "fireplace_qu": 3.0,
  "fireplaces": 1,
  "overall_cond": 5,
  "garage_cars": 2.0,
  "lot_area": 8500.0,
  "garage_cond": 3.0,
  "garage_area": 400.0,
  "central_air_N": "0",
  "bsmt_fin_sf_1": 450.0,
  "heating_qc": 5.0,
  "central_air_Y": "1"
}

Response body

{
  "estimated_price": 356280.87,
  "currency": "USD"
}


6.System Architecture

The project follows a modular architecture to ensure scalability and separation of concerns:

Data Layer: Raw CSV data is ingested, cleaned, and stored in a PostgreSQL container.
Processing Layer: Feature engineering and model training are performed via Jupyter Notebooks, pulling data directly from SQL.
Model Layer: The trained CatBoost model and feature importance list are serialized using joblib.
Service Layer: A FastAPI application loads the model and serves a /predict endpoint.
Deployment: The entire stack is containerized using Docker and Docker Compose.


7.Tech Stack

Language: Python 3.12
Database: PostgreSQL 15
API Framework: FastAPI (Pydantic for validation)
ML Libraries: Scikit-learn, CatBoost, Pandas, NumPy
Containerization: Docker & Docker Compose
Environment: .env for secure credential management


8.How to Run

Using Docker (The Easiest Way)

Build the image:
Bash

docker build -t ames-housing-app .

Run the container:
Bash

docker run -p 10000:10000 ames-housing-app
Go to http://localhost:10000/docs in your browser to test it!

Manual Way

If you don't have Docker, just install the requirements:
Bash

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 10000

9.Contact

If you have questions, check my GitHub: https://github.com/Alihmidov