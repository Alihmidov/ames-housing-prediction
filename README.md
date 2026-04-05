Ames Housing Price Prediction Project

## 🔗 Quick Links
* **🚀 Live API Demo:** [https://ames-housing-prediction.onrender.com/docs](https://ames-housing-prediction.onrender.com/docs)
* **💻 Project Repository:** [https://github.com/Alihmidov/ames-housing-prediction](https://github.com/Alihmidov/ames-housing-prediction)
* **👤 GitHub Profile:** [https://github.com/Alihmidov](https://github.com/Alihmidov)


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

Live Demo & Deployment

The project is fully containerized and deployed on the Render cloud platform. This allows users to interact with the model in real-time without any local setup.
Access Live API (Swagger UI)

How to perform a live test:

    Click the link above to open the API documentation.

    Locate the POST /predict endpoint.

    Click "Try it out".

    Use the default JSON values and click "Execute".

    Check the "Server Response" to see the predicted house price!

Infrastructure & Security

This project demonstrates a production-grade machine learning lifecycle:

    Database: A managed PostgreSQL instance on Render stores the cleaned dataset.

    Containerization: The application is packaged using Docker, ensuring consistency between development and production.

    CI/CD: Automated builds are triggered on every push to the main branch.

    Security: The database is protected with Inbound IP Restrictions, allowing only the internal API service to connect.




If you want to run the project locally on your machine, follow these steps:

### Using Docker (Recommended)
1. **Build the image:**
   ```bash
   docker build -t ames-housing-app .

    Run the container:
    Bash

    docker run -p 10000:10000 ames-housing-app

    Access the API: Once the container is running, open your browser at http://localhost:10000/docs.

Manual Installation
Bash

pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 10000

Conclusion

This project transitions from a simple Jupyter Notebook exploration to a fully integrated End-to-End Machine Learning System. By focusing on model generalization (CatBoost) and robust deployment (Docker/FastAPI), it provides a scalable and secure solution for real estate valuation.

Contact: GitHub Profile | Project Repository
9.Contact

If you have questions, check my GitHub: https://github.com/Alihmidov