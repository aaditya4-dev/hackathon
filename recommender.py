import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import hstack


def train_recommender(df):

    df_rec = df.copy()

    df_rec['genres'] = df_rec['genres'].fillna('')
    df_rec['pages'] = pd.to_numeric(df_rec['pages'], errors='coerce').fillna(df_rec['pages'].median())
    df_rec['rating'] = pd.to_numeric(df_rec['rating'], errors='coerce').fillna(df_rec['rating'].median())
    df_rec['likedPercent'] = pd.to_numeric(df_rec['likedPercent'], errors='coerce').fillna(df_rec['likedPercent'].median())

    # TF-IDF on genres
    tfidf = TfidfVectorizer(stop_words='english', max_features=100)
    genre_matrix = tfidf.fit_transform(df_rec['genres'])

    # numerical features
    scaler = MinMaxScaler()
    num_features = scaler.fit_transform(df_rec[['pages', 'rating', 'likedPercent']])

    # combine features
    book_dna = hstack([genre_matrix, num_features * 0.5])

    # train KNN
    knn_model = NearestNeighbors(
        n_neighbors=11,
        algorithm='brute',
        metric='cosine'
    )

    knn_model.fit(book_dna)

    return knn_model, book_dna, df_rec