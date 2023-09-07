import json
from langdetect import detect
from collections import Counter

# Path to your file
file_path = 'conv_sample'

def truncate_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + '...'

def extract_text_from_data(data):
    try:
        post_list = data.get('post_list', [])
        if post_list:
            first_post = post_list[0]
            return first_post.get('text', 'Text not found')
        else:
            return 'No posts in the list'
    except KeyError:
        return 'Text extraction error'

def main():
    start_line = 1
    num_datapoints = 1000  # Number of data points to iterate through
    max_text_length = 100  # Maximum number of characters to display
    
    detected_languages = Counter()

    with open(file_path, 'r') as file:
        data_lines = file.readlines()

    for line_number in range(start_line, start_line + num_datapoints):
        if line_number <= len(data_lines):
            data_line = data_lines[line_number - 1]
            try:
                json_data = json.loads(data_line.strip())  # Strip newline characters
                
                text = extract_text_from_data(json_data)
                truncated_text = truncate_text(text, max_text_length)
                
                detected_language = detect(text)
                detected_languages[detected_language] += 1
                
                print(f"Data Point {line_number} Text: {truncated_text}")
                print(f"LANGUAGE: {detected_language}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON for Data Point {line_number}")
        else:
            print(f"Line {line_number} is beyond the available data lines.")
    
    total_detected = sum(detected_languages.values())
    print("\nLanguage Detection Statistics:")
    for lang, count in detected_languages.items():
        percentage = (count / total_detected) * 100
        print(f"{lang.upper()}: {percentage:.2f}%")

if __name__ == "__main__":
    main()
