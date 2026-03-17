from fastapi import APIRouter
from services.analysis import load_data, predictor_model, predictor_features
from model.predictor import predict_demand
import pandas as pd
from database.db import conn
from collections import Counter

router = APIRouter()


# TRENDING BOOKS
@router.get("/seller/trending")
def trending_books():
  
   df = load_data()

   df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
   df['numRatings'] = pd.to_numeric(df['numRatings'], errors='coerce').fillna(0)
   df['likedPercent'] = pd.to_numeric(df['likedPercent'], errors='coerce').fillna(0)

# normalize
   df["rating_norm"] = df["rating"] / df["rating"].max()
   df["ratings_norm"] = df["numRatings"] / df["numRatings"].max()
   df["likes_norm"] = df["likedPercent"] / df["likedPercent"].max()

# trend score
   df["trend_score"] = (
      df["rating_norm"] * 0.4 +
      df["ratings_norm"] * 0.4 +
      df["likes_norm"] * 0.2
    )

   trending = df.sort_values("trend_score", ascending=False).head(10)
   return {
        "trending_books": trending[['title','trend_score']].to_dict(orient="records")
    }


# SELLER ANALYTICS
@router.get("/seller/analytics")
def seller_analytics():

    df = load_data()

    total_books = len(df)

    avg_rating = df["rating"].mean()

    top_genres = (
        df["genres"]
        .str.split(",")
        .explode()
        .value_counts()
        .head(3)
        .index
        .tolist()
    )

    top_books = (
        df.sort_values("numRatings", ascending=False)
        .head(5)["title"]
        .tolist()
    )

    return {
        "total_books": total_books,
        "average_rating": round(avg_rating,2),
        "top_genres": top_genres,
        "top_books": top_books
    }


# DEMAND PREDICTION (AI MODEL)
@router.get("/seller/predict-demand")
def predict_demand_endpoint():

    df = load_data()

    predictions = predict_demand(predictor_model, predictor_features, df)

    return {
        "predicted_trending_books":
        predictions[['title','demand_score']].to_dict(orient="records")
    }
@router.get("/seller/user-insights")
def user_insights():

    cursor = conn.cursor()

    cursor.execute("SELECT book FROM user_reads")

    rows = cursor.fetchall()

    books = [row[0] for row in rows]

    counts = Counter(books)

    top_books = counts.most_common(5)

    return {
        "books_users_are_reading": top_books
    }