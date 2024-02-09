import hashlib

def sort_characters(text):
    stop_words = ["University", "of", "Institute"]
    cleaned_text = ' '.join(word for word in text.split() if word not in stop_words)
    alphabet_chars = ''.join(char for char in cleaned_text if char.isalpha())
    sorted_text = ''.join(sorted(alphabet_chars))
    return sorted_text

def hashed(input_string):
    sha256 = hashlib.sha256()
    new_string = sort_characters(input_string)
    sha256.update(new_string.encode())
    hashed_value = int(sha256.hexdigest(), 16)
    return hashed_value