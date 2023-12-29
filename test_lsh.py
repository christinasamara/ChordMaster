from lsh import lsh
import numpy as np
import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

df = pd.read_csv("data.csv")
dfres = df.copy()
df['SURNAME'] = df['SURNAME'].apply(lambda x: ord(x[0].lower()))

lsh(dfres)


