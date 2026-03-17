import pandas as pd
from recommender import train_recommender
from backend.model.predictor import train_predictor

# load data
df = pd.read_csv("data/final_merge.csv")

# train models
knn_model, book_dna, df_rec = train_recommender(df)

rf_model, expected_cols, genres, threshold, stats = train_predictor(df)

print("Models trained successfully")