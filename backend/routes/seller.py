from fastapi import APIRouter
from services.analysis import load_data, predictor_model, predictor_features
from model.predictor import predict_demand

router = APIRouter()

@router.get("/seller/trending")
def trending_books():

    trending = [
        "Atomic Habits",
        "Rich Dad Poor Dad",
        "The Alchemist",
        "Deep Work"
    ]

    return {
        "trending_books": trending
    }
@router.get("/seller/analytics")
def seller_analytics():

    analytics = {
        "top_genres": ["Self Help", "Finance", "Fiction"],
        "top_books": ["Atomic Habits", "Deep Work"],
        "low_demand_books": ["Old Classics"]
    }

    return analytics 


@router.get("/seller/predict-demand")
def predict_demand_endpoint():

    df = load_data()

    predictions = predict_demand(predictor_model, predictor_features, df)

    return {
        "predicted_trending_books": predictions[['title','demand_score']].to_dict(orient="records")
    }