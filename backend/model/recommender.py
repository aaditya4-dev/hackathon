import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import hstack
from scipy.sparse import csr_matrix


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
    num_features_sparse = csr_matrix(num_features * 0.5)

    book_dna = hstack([genre_matrix, num_features_sparse])

    # train KNN
    knn_model = NearestNeighbors(
        n_neighbors=11,
        algorithm='brute',
        metric='cosine'
    )

    knn_model.fit(book_dna)

    return knn_model, book_dna, df_rec

def get_recommendations(book_title, knn_model, book_dna, df_rec, k=5):

    book_title = book_title.lower()
    df_rec['title_lower'] = df_rec['title'].str.lower()

    if book_title not in df_rec['title_lower'].values:
        return ["Book not found"]

    idx = df_rec[df_rec['title_lower'] == book_title].index[0]
   

    distances, indices = knn_model.kneighbors(book_dna[idx], n_neighbors=k+1)

    rec_indices = indices.flatten()[1:]

    recommendations = df_rec.iloc[rec_indices]['title'].tolist()

    return recommendations