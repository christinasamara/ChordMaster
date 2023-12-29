import re
from difflib import SequenceMatcher
import pandas as pd
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data loading
my_stop_words = ["university", "of", "institute"]
df = pd.read_csv("data.csv")
df_education = df['EDUCATION']

# Sample query universities
query_universities = ["Cornell University", "Princeton University", "California", "MIT"]

# Concatenate the education data into a single string
all_education_text = ' '.join(df_education)

# Combine the education data and query for TF-IDF vectorization
documents = [all_education_text] + query_universities

# TF-IDF vectorization with stopwords
vectorizer = TfidfVectorizer(stop_words=my_stop_words)
tfidf_matrix = vectorizer.fit_transform(documents)

# Calculate cosine similarity
cosine_similarities = cosine_similarity(tfidf_matrix[1:], tfidf_matrix[0].reshape(1, -1))

# Print the results
for i, query in enumerate(query_universities):
    similarity = cosine_similarities[i][0]
    print(f"Similarity with query '{query}': {similarity}")
