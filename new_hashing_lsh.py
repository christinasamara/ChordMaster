import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.neighbors import NearestNeighbors
from lsh import lsh
import pandas as pd
import hashlib

my_stop_words = ["University", "of", "Institute"]

from sklearn.feature_extraction.text import TfidfVectorizer

def hash_tfidf_string(tfidf_string):
    tfidf_vectorizer = TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(5, 6),
        min_df=0,
        stop_words=my_stop_words
    )
    X_tfidf = tfidf_vectorizer.fit_transform([tfidf_string])
    X_array = X_tfidf.toarray()

    hashed_value = hash(X_array.tobytes())

    return hashed_value

def lsh_with_chord_single_string(input_string, chord_ring_size=16):
    hashed_education = hash_tfidf_string(input_string)
    chord_key = hashed_education % chord_ring_size

    return chord_key

def sort_characters(text):
    # Remove whitespaces and single quotes
    cleaned_text = text.replace(' ', '').replace("'", '')
    sorted_text = ''.join(sorted(cleaned_text))
    return sorted_text

def sha256_hash(input_string):
    sha256 = hashlib.sha256()
    new_string = sort_characters(input_string)
    sha256.update(new_string.encode())
    hashed_value = int(sha256.hexdigest(), 16)
    return hashed_value

if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    df_education = df['EDUCATION']
    for i in df_education:
        chord_key = sha256_hash(i) % 16
        print(f"Chord key for '{i}': {chord_key}")

# for hashing: firstly sort the string and then hash it with sha256