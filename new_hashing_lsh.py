import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.neighbors import NearestNeighbors
from lsh import lsh
import pandas as pd

my_stop_words = ["University", "of", "Institute"]

def hash_tfidf_matrix(X_tfidf):
    # Convert the sparse matrix to a dense array before hashing
    X_array = X_tfidf.toarray()

    # Hash the entire array
    hashed_value = hash(X_array.tobytes())

    return hashed_value

def lsh_with_chord(df, chord_ring_size=16):
    # Vectorize education strings
    tfidf_vectorizer = TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(4, 5),
        min_df=0,
        stop_words=my_stop_words
    )
    chord_keys = []

    for index, row in df.iterrows():
        X_tfidf = tfidf_vectorizer.fit_transform([row['EDUCATION']])

        # Hash the TF-IDF matrix into a single integer
        hashed_education = hash_tfidf_matrix(X_tfidf)

        # Map the hashed value to the Chord ring space
        chord_key = hashed_education % chord_ring_size

        chord_keys.append(chord_key)

    # Add the Chord keys as a new column to the DataFrame
    df['Chord_Key'] = chord_keys

    return df

# Example usage:
df = pd.read_csv("data.csv")
df_education = df[['EDUCATION']]

result_df = lsh_with_chord(df_education)
result_df.to_csv("result_data.csv", index=False)
