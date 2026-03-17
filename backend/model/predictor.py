import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_predictor(df):

    model_df = df[['genres','pages','price','numRatings','numofchar']].copy()
    model_df = model_df.dropna()

    # clean genres
    model_df['genres'] = model_df['genres'].str.replace('[', '', regex=False)\
                                           .str.replace(']', '', regex=False)\
                                           .str.replace("'", '', regex=False)

    model_df['genres'] = model_df['genres'].str.split(',')
    model_df = model_df.explode('genres')
    model_df['genres'] = model_df['genres'].str.strip()


    # bestseller threshold
    threshold = model_df['numRatings'].quantile(0.80)

    model_df['Bestseller'] = (model_df['numRatings'] > threshold).astype(int)

    # valid genres
    listofgenre = [
        'Fantasy','Fiction','Young Adult','Audiobook','Horror','Novels',
        'Romance','Adult','Historical','Adventure','Action','Crime',
        'Comedy','Vampires','War','Drama','Dragons'
    ]

    model_df = model_df[model_df['genres'].isin(listofgenre)]

    # bestseller averages
    bestseller_stats = model_df[model_df['Bestseller'] == 1]\
        .groupby('genres')[['pages', 'price']]\
        .mean()\
        .to_dict('index')

    # ML preprocessing
    model_df = model_df[['pages','price','numofchar','genres','Bestseller']]
    model_df = pd.get_dummies(model_df, columns=['genres'], dtype=int)

    X = model_df.drop('Bestseller', axis=1)
    y = model_df['Bestseller']

    # train model
    model = RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        max_depth=12,
        class_weight='balanced'
    )

    model.fit(X, y)

    return model, X.columns, listofgenre, threshold, bestseller_stats

def predict_demand(model, features, df, top_n=10):

    model_df = df[['genres','pages','price','numRatings','numofchar']].copy()
    model_df = model_df.dropna()

    model_df['genres'] = model_df['genres'].str.replace('[', '', regex=False)\
                                           .str.replace(']', '', regex=False)\
                                           .str.replace("'", '', regex=False)

    model_df['genres'] = model_df['genres'].str.split(',')
    model_df = model_df.explode('genres')
    model_df['genres'] = model_df['genres'].str.strip()

    model_df = pd.get_dummies(model_df[['pages','price','numofchar','genres']], dtype=int)

    model_df = model_df.reindex(columns=features, fill_value=0)

    probs = model.predict_proba(model_df)[:,1]

    model_df["demand_score"] = probs

    # merge exploded rows back to books
    scores = model_df.groupby(model_df.index)["demand_score"].mean()

    df_copy = df.copy()
    df_copy["demand_score"] = scores

    return df_copy.sort_values("demand_score", ascending=False).head(top_n)