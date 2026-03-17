import pandas as pd
from model.recommender import train_recommender
from model.predictor import train_predictor

DATA_PATH = "data/final_merge.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Train recommender model
knn_model, book_dna, df_rec = train_recommender(df)

# Train predictor model
predictor_model, predictor_features, genres, threshold, stats = train_predictor(df)

def load_data():
    return df

print(df['title'].head(20))