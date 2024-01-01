import mmh3  # MurmurHash3 library, install using: pip install mmh3
import pandas as pd

class MinHash:
    def __init__(self, num_hashes, range_max):
        self.num_hashes = num_hashes
        self.range_max = range_max

    def hash_function(self, data):
        return mmh3.hash(data)

    def min_hash_single_item(self, item):
        if not item:
            raise ValueError("Input item is empty.")

        hash_values = [float('inf')] * self.num_hashes

        for i in range(self.num_hashes):
            combined_data = f"{i}-{item}"
            hash_value = self.hash_function(combined_data)
            hash_values[i] = min(hash_values[i], hash_value)

        return min(hash_values) % self.range_max

# Example usage:
if __name__ == "__main__":
    minhash = MinHash(num_hashes=100, range_max=16)

    # Example string to hash
    input_string = "example_item"

    df = pd.read_csv("data.csv")
    df_education = df['EDUCATION']
    for i in df_education:
        minhash_value = minhash.min_hash_single_item(i)
        print(f"MinHash value for '{i}': {minhash_value}")

