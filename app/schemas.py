from pydantic import BaseModel

class HouseInput(BaseModel):
    total_living_area: float
    overall_qual: int
    gr_liv_area: float
    exter_qual: float
    kitchen_qual: float
    total_bathrooms: float
    year_built: int
    bsmt_qual: float
    house_age: int
    fireplace_qu: float
    fireplaces: int
    overall_cond: int
    garage_cars: float
    lot_area: float
    garage_cond: float
    garage_area: float
    central_air_n: str  
    bsmt_fin_sf_1: float
    heating_qc: float
    central_air_y: str

class PredictionOutput(BaseModel):
    estimated_price: float
    currency: str = "USD"
    message: str = "Prediction successful"