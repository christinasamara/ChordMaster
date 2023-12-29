import csv
import hashlib

def create_hash(input_string):
    # Using SHA-256 as an example
    hash_object = hashlib.sha256(input_string.encode())
    hash_value = hash_object.hexdigest()
    return hash_value

def hash_name(name):
    return int(hashlib.sha256(name.encode()).hexdigest(), 16)

hashed_names = []
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(hash_name(row[0]))

