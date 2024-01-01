def sort_string(input_string):
    sorted_chars = sorted(input_string)
    sorted_string = ''.join(sorted_chars)
    return sorted_string

# Example usage:
if __name__ == "__main__":
    input_string = "example_input_string"
    
    sorted_result = sort_string(input_string)
    print(f"Original String: {input_string}")
    print(f"Sorted String: {sorted_result}")